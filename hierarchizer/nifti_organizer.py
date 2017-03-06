import logging
import shutil
from os import path
from os import makedirs
from os import listdir
from glob import iglob


def organize_nifti(args):
    logging.info("Organizing NIFTI files...")
    if args.dataset.upper() == 'CLM':
        organize_nifti_clm(args.input_folder, args.output_folder)
    elif args.dataset.upper() == 'EDSD':
        organize_nifti_edsd(args.input_folder, args.output_folder)


def organize_nifti_clm(input_folder, output_folder):
    logging.info("Call to organize_nifti_clm")

    anat_folder_label = "T1_mprage"
    repetition_folder_name = "1"

    for nii_file in iglob(path.join(input_folder, "**/*.nii"), recursive=True):
        logging.info("Processing %s..." % nii_file)

        subject_id = split(r'[_.]+', path.basename(nii_file))[1]
        directory = path.join(output_folder, subject_id)
        makedirs(directory, exist_ok=True)
        num_subdirs = len(listdir(directory)) + 1
        output_fullpath = path.join(directory, str(num_subdirs), anat_folder_label, repetition_folder_name)
        makedirs(output_fullpath, exist_ok=True)

        logging.info("Copying %s to %s..." % (nii_file, output_fullpath))
        shutil.copy2(nii_file, output_fullpath)

    logging.info("DONE")


def organize_nifti_edsd(input_folder, output_folder):
    logging.info("Call to organize_nifti_edsd")

    for archive_path in iglob(path.join(input_folder, "**/*.tar.bz2"), recursive=True):
        logging.info("Processing %s..." % archive_path)

        file_info = split(r'[+.]+', path.basename(archive_path))
        site = file_info[2]
        subject_id = site + "_" + file_info[3]
        directory = path.join(output_folder, subject_id)
        label_session = file_info[7]
        session_folder = path.join(directory, label_session)
        anat_folder_label = file_info[5]
        protocol_folder = path.join(session_folder, anat_folder_label)
        makedirs(protocol_folder, exist_ok=True)
        num_subdirs = len(listdir(protocol_folder)) + 1
        repetition_folder = path.join(protocol_folder, str(num_subdirs))
        makedirs(repetition_folder, exist_ok=True)

        logging.info("Extracting %s to %s..." % (archive_path, repetition_folder))
        tar = shutil.tarfile.open(archive_path, "r:bz2")
        tar.extractall(path=repetition_folder)
        tar.close()
        fullpath = path.join(repetition_folder, listdir(repetition_folder)[0])
        for f in iglob(fullpath + "/**.nii", recursive=True):
            shutil.move(f, repetition_folder)
            shutil.rmtree(fullpath)

        # TODO : write this in a more generic and proper way
        with open(path.join(repetition_folder, "meta.xml"), 'w') as f:
            f.write("<siteKey>" + site + "</siteKey>")

    logging.info("DONE")


def organize_nifti_adni(input_folder, output_folder):
    logging.info("Call to organize_nifti_adni")
    for nii_file in iglob(path.join(input_folder, "**/*.nii"), recursive=True):
        f_name = split(r'[_]+', path.basename(nii_file))
        subject_id = '_'.join(f_name[1:4])
        session = f_name[-3][:8]
        image_id = split(r'[.]+', f_name[-1])[0][1:]
        protocol = '_'.join(f_name[f_name.index("MR") + 1:f_name.index("Br")])
        repetition_folder = path.join(output_folder, subject_id, session, protocol, image_id)
        makedirs(repetition_folder, exist_ok=True)
        shutil.copy2(nii_file, repetition_folder)
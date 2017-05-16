import logging
import shutil
from os import path
from os import makedirs
from os import listdir
from os.path import isdir
from glob import iglob
from re import split

DEFAULT_ORGANIZATION = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']
CLM_NIFTI_ALLOWED_FIELDS = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']
EDSD_NIFTI_ALLOWED_FIELDS = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']
ADNI_NIFTI_ALLOWED_FIELDS = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']


def organize_nifti(incoming_dataset, input_folder, output_folder, organisation, meta_output_folder):
    logging.info("Organizing NIFTI files...")
    if incoming_dataset == 'CLM':
        if not _is_organisation_allowed(organisation, CLM_NIFTI_ALLOWED_FIELDS):
            logging.warning("Not enough information available: falling back to default organisation !")
            organisation = DEFAULT_ORGANIZATION
        organize_nifti_clm(input_folder, output_folder, organisation, meta_output_folder)
    elif incoming_dataset == 'EDSD':
        if not _is_organisation_allowed(organisation, EDSD_NIFTI_ALLOWED_FIELDS):
            logging.warning("Not enough information available: falling back to default organisation !")
            organisation = DEFAULT_ORGANIZATION
        organize_nifti_edsd(input_folder, output_folder, organisation, meta_output_folder)
    elif incoming_dataset == 'ADNI':
        if not _is_organisation_allowed(organisation, ADNI_NIFTI_ALLOWED_FIELDS):
            logging.warning("Not enough information available: falling back to default organisation !")
            organisation = DEFAULT_ORGANIZATION
        organize_nifti_adni(input_folder, output_folder, organisation, meta_output_folder)


def organize_nifti_clm(input_folder, output_folder, organisation, meta_output_folder):
    logging.info("Call to organize_nifti_clm")

    default_protocol = "T1_mprage"
    default_repetition = "1"

    for nii_file in iglob(path.join(input_folder, "**/*.nii"), recursive=True):
        logging.info("Processing %s..." % nii_file)

        metadata = dict()
        metadata['SeriesDescription'] = default_protocol
        metadata['SeriesNumber'] = default_repetition
        metadata['StudyID'], tmp = path.basename(nii_file).split('_')
        metadata['PatientID'] = tmp[:-4]

        output_fullpath = output_folder
        for attribute in organisation:
            output_fullpath = path.join(output_fullpath, metadata[attribute])

        makedirs(output_fullpath, exist_ok=True)
        logging.info("Copying %s to %s..." % (nii_file, output_fullpath))
        shutil.copy2(nii_file, output_fullpath)

    meta_file = next(iglob(path.join(input_folder, '**/public_output.xlsx'), recursive=True))
    shutil.copy2(meta_file, meta_output_folder)

    logging.info("DONE")


def organize_nifti_edsd(input_folder, output_folder, organisation, meta_output_folder):
    logging.info("Call to organize_nifti_edsd")

    for archive_path in iglob(path.join(input_folder, "**/*.tar.bz2"), recursive=True):
        logging.info("Processing %s..." % archive_path)

        file_info = split(r'[+.]+', path.basename(archive_path))
        prefix = file_info[0] + '+'
        site = file_info[2][:3]
        sid_per_site = file_info[3]
        proto = file_info[4]

        metadata = dict()
        metadata['PatientID'] = prefix + site + proto + sid_per_site
        metadata['StudyID'] = file_info[7]
        metadata['SeriesDescription'] = file_info[5]
        protocol_folder = path.join(
            output_folder, metadata['PatientID'], metadata['StudyID'], metadata['SeriesDescription'])
        makedirs(protocol_folder, exist_ok=True)
        metadata['SeriesNumber'] = str(len(listdir(protocol_folder)) + 1)
        output_fullpath = path.join(protocol_folder, metadata['SeriesNumber'])
        makedirs(output_fullpath, exist_ok=True)

        logging.info("Extracting %s to %s..." % (archive_path, output_fullpath))
        tar = shutil.tarfile.open(archive_path, "r:bz2")
        tar.extractall(path=output_fullpath)
        tar.close()

        for meta_file in iglob(path.join(output_fullpath, "**/*.txt"), recursive=True):
            meta_filename = _fix_edsd_site_in_filename(path.basename(meta_file))
            shutil.move(meta_file, path.join(meta_output_folder, meta_filename))

        extracted_fullpath = path.join(output_fullpath, listdir(output_fullpath)[0])
        if isdir(extracted_fullpath):
            for f in iglob(extracted_fullpath + "/**.nii", recursive=True):
                output_fullpath = output_folder
                for attribute in organisation:
                    output_fullpath = path.join(output_fullpath, metadata[attribute])
                makedirs(output_fullpath, exist_ok=True)
                output_filename = _fix_edsd_site_in_filename(path.basename(f))
                output_fullpath = path.join(output_fullpath, output_filename)
                shutil.move(f, output_fullpath)
            shutil.rmtree(extracted_fullpath)

    logging.info("DONE")


def organize_nifti_adni(input_folder, output_folder, organisation, meta_output_folder):
    logging.info("Call to organize_nifti_adni")

    for nii_file in iglob(path.join(input_folder, "**/*.nii"), recursive=True):
        f_name = split(r'[_]+', path.basename(nii_file))

        metadata = dict()
        metadata['PatientID'] = '_'.join(f_name[1:4])
        metadata['StudyID'] = f_name[-3][:8]
        metadata['SeriesDescription'] = '_'.join(f_name[f_name.index("MR") + 1:f_name.index("Br")])
        metadata['SeriesNumber'] = split(r'[.]+', f_name[-1])[0][1:]

        output_fullpath = output_folder
        for attribute in organisation:
            output_fullpath = path.join(output_fullpath, metadata[attribute])

        makedirs(output_fullpath, exist_ok=True)
        logging.info("Copying %s to %s..." % (nii_file, output_fullpath))
        shutil.copy2(nii_file, output_fullpath)

    for meta_file in iglob(path.join(input_folder, "**/*.xml"), recursive=True):
        shutil.move(meta_file, meta_output_folder)

    logging.info("DONE")


def _fix_edsd_site_in_filename(filename):
    file_parts = split(r'[+]+', filename)
    file_parts[2] = file_parts[2][:3]
    file_parts[-1] = file_parts[-1][:3]
    fixed_filename = '+'.join(file_parts) + '.nii'
    return fixed_filename


def _is_organisation_allowed(organisation, allowed_fields):
    for field in organisation:
        if field not in allowed_fields:
            return False
    return True

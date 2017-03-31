import logging
import shutil
from os import path
from os import makedirs
from os import listdir
from glob import iglob
from re import split

DEFAULT_ORGANIZATION = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']
CLM_NIFTI_ALLOWED_FIELDS = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']
EDSD_NIFTI_ALLOWED_FIELDS = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']
ADNI_NIFTI_ALLOWED_FIELDS = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']


def organize_nifti(incoming_dataset, input_folder, output_folder, organisation):
    logging.info("Organizing NIFTI files...")
    if incoming_dataset.upper() == 'CLM':
        if not _is_organisation_allowed(organisation, CLM_NIFTI_ALLOWED_FIELDS):
            organisation = DEFAULT_ORGANIZATION
        organize_nifti_clm(input_folder, output_folder, organisation)
    elif incoming_dataset.upper() == 'EDSD':
        if not _is_organisation_allowed(organisation, EDSD_NIFTI_ALLOWED_FIELDS):
            organisation = DEFAULT_ORGANIZATION
        organize_nifti_edsd(input_folder, output_folder, organisation)
    elif incoming_dataset.upper() == 'ADNI':
        if not _is_organisation_allowed(organisation, ADNI_NIFTI_ALLOWED_FIELDS):
            organisation = DEFAULT_ORGANIZATION
        organize_nifti_adni(input_folder, output_folder, organisation)


def organize_nifti_clm(input_folder, output_folder, organisation):
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
            output_folder += path.join(output_fullpath, metadata[attribute])

        makedirs(output_fullpath, exist_ok=True)
        logging.info("Copying %s to %s..." % (nii_file, output_fullpath))
        shutil.copy2(nii_file, output_fullpath)

    logging.info("DONE")


def organize_nifti_edsd(input_folder, output_folder, organisation):
    logging.info("Call to organize_nifti_edsd")

    for archive_path in iglob(path.join(input_folder, "**/*.tar.bz2"), recursive=True):
        logging.info("Processing %s..." % archive_path)

        file_info = split(r'[+.]+', path.basename(archive_path))
        prefix = "ng+"
        site = file_info[2]
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

        extracted_fullpath = path.join(output_fullpath, listdir(output_fullpath)[0])
        for f in iglob(extracted_fullpath + "/**.nii", recursive=True):
            output_fullpath = output_folder
            for attribute in organisation:
                output_folder += path.join(output_fullpath, metadata[attribute])
            makedirs(output_fullpath, exist_ok=True)
            shutil.move(f, output_fullpath)
        shutil.rmtree(extracted_fullpath)

    logging.info("DONE")


def organize_nifti_adni(input_folder, output_folder, organisation):
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
            output_folder += path.join(output_fullpath, metadata[attribute])

        makedirs(output_fullpath, exist_ok=True)
        logging.info("Copying %s to %s..." % (nii_file, output_fullpath))
        shutil.copy2(nii_file, output_fullpath)


def _is_organisation_allowed(organisation, allowed_fields):
    for field in organisation:
        if field not in allowed_fields:
            return False
    return True

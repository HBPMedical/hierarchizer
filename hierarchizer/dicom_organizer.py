import logging
from glob import iglob
from os import path
from os import makedirs
from shutil import copy2
import dicom  # pydicom
from dicom.errors import InvalidDicomError  # pydicom.errors.InvalidDicomError

from . import ppmi_xml_extension


def organize_dicom(args):
    logging.info("Organizing DICOM files...")
    for file_path in iglob(path.join(args.input_folder, "**/*"), recursive=True):
        try:
            dcm = dicom.read_file(file_path)
            dest_path = args.output_folder
            for attribute in args.output_folder_organization:
                part = str(dcm.data_element(attribute).value)
                if len(part.strip()) < 1 or attribute in args.excluded_fields:
                    part = None
                    if args.ppmi_xml_extension:
                        part = ppmi_xml_extension.find(file_path, attribute)
                    if not part:
                        part = args.unknown_value
                dest_path += "/" + part
            dest_path = path.normpath(dest_path)
            makedirs(dest_path, exist_ok=True)
            logging.info("Copying %s to %s..." % (file_path, dest_path))
            copy2(file_path, dest_path)
        except (IsADirectoryError, InvalidDicomError):
            pass

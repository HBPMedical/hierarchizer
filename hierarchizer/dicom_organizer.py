import logging
from glob import iglob
from os import path
from os import makedirs
from shutil import copy2
import dicom  # pydicom
from dicom.errors import InvalidDicomError  # pydicom.errors.InvalidDicomError

from . import ppmi_xml_extension


def organize_dicom(input_folder, output_folder, organisation, excluded_fields, use_ppmi_xml_extension, unknown_value):
    logging.info("Organizing DICOM files...")
    for file_path in iglob(path.join(input_folder, "**/*"), recursive=True):
        try:
            dcm = dicom.read_file(file_path)
            for attribute in organisation:
                try:
                    part = str(dcm.data_element(attribute).value)
                except AttributeError:
                    part = None
                if not part or len(part.strip()) < 1 or attribute in excluded_fields:
                    part = None
                    if use_ppmi_xml_extension:
                        part = ppmi_xml_extension.find(file_path, attribute)
                    if not part:
                        part = unknown_value
                output_folder = path.join(output_folder, part)
            makedirs(output_folder, exist_ok=True)
            logging.info("Copying %s to %s..." % (file_path, output_folder))
            copy2(file_path, output_folder)
        except (IsADirectoryError, InvalidDicomError):
            pass

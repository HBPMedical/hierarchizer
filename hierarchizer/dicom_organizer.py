import logging
from glob import iglob
from os import path, makedirs
from shutil import copy2
import dicom  # pydicom
from dicom.errors import InvalidDicomError  # pydicom.errors.InvalidDicomError

from . import ppmi_xml_extension


def organize_dicom(input_folder, output_folder, organisation, excluded_fields, use_ppmi_xml_extension,
                   unknown_value, allowed_field_values):
    logging.info("Organizing DICOM files...")
    for file_path in iglob(path.join(input_folder, "**/*"), recursive=True):
        output_fullpath = output_folder
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
                if attribute in allowed_field_values:
                    if part in allowed_field_values[attribute]:
                        logging.info("Skipping files in %s..." % output_fullpath)
                        continue

                output_fullpath = path.join(output_fullpath, part.replace('/', '_'))
                output_fullpath = output_fullpath.replace('*', '_')
            makedirs(output_fullpath, exist_ok=True)
            logging.info("Copying %s to %s..." % (file_path, output_fullpath))
            copy2(file_path, output_fullpath)
        except (IsADirectoryError, InvalidDicomError):
            pass

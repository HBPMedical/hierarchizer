#!/usr/bin/env python3.5

import argparse
import logging
import dicom
from glob import iglob
from os import makedirs
from os import path
from shutil import copy2
from dicom.errors import InvalidDicomError

import ppmi_xml_extension


DEFAULT_PPMI_EXCLUDED_FIELDS = ['StudyID', 'SeriesNumber']


def main():
    logging.basicConfig(level=logging.INFO)

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("input_folder")
    args_parser.add_argument("output_folder")
    args_parser.add_argument("--attributes",
                             nargs='+',
                             default=['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber'])
    args_parser.add_argument("--unknown_value", default="unknown")
    args_parser.add_argument("--ppmi_xml_extension", action='store_true')
    args_parser.add_argument("--excluded_fields", nargs='+', default=[])
    args = args_parser.parse_args()

    if args.ppmi_xml_extension and not args.excluded_fields:
        excluded_fields = DEFAULT_PPMI_EXCLUDED_FIELDS

    for file_path in iglob(path.join(args.input_folder, "**/*"), recursive=True):
        try:
            dcm = dicom.read_file(file_path)
            dest_path = args.output_folder
            for attribute in args.attributes:
                part = str(dcm.data_element(attribute).value)
                if len(part.strip()) < 1 or attribute in excluded_fields:
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


if __name__ == '__main__':
    main()

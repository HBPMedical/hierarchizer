#!/usr/bin/env python3.5

import logging
import argparse
import dicom
from os import path
from os import makedirs
from shutil import copy2
from glob import iglob
from dicom.errors import InvalidDicomError


HIERARCHY = ['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber']
UNKNOWN_VALUE = "unknown"


def main():
    logging.basicConfig(level=logging.INFO)

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("input_folder")
    args_parser.add_argument("output_folder")
    args = args_parser.parse_args()

    for file_path in iglob(path.join(args.input_folder, "**/*"), recursive=True):
        try:
            dcm = dicom.read_file(file_path)
            dest_path = args.output_folder
            for attribute in HIERARCHY:
                part = str(dcm.data_element(attribute).value)
                if len(part) < 1:
                    part = UNKNOWN_VALUE
                dest_path += "/" + part
            dest_path = path.normpath(dest_path)
            makedirs(dest_path, exist_ok=True)
            copy2(file_path, dest_path)
        except (IsADirectoryError, InvalidDicomError):
            pass


if __name__ == '__main__':
    main()

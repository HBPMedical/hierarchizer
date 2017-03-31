#!/usr/bin/env python3.5

import argparse
import logging
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from hierarchizer import ppmi_xml_extension
from hierarchizer import dicom_organizer
from hierarchizer import nifti_organizer


def main():
    logging.basicConfig(level=logging.INFO)

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("input_folder")
    args_parser.add_argument("output_folder")
    args_parser.add_argument("--incoming_dataset", default="generic")
    args_parser.add_argument("--type", default="DICOM")
    args_parser.add_argument("--output_folder_organisation",
                             default='#PatientID/#StudyID/#SeriesDescription/#SeriesNumber')
    args_parser.add_argument("--unknown_value", default="unknown")
    args_parser.add_argument("--ppmi_xml_extension", action='store_true')
    args_parser.add_argument("--excluded_fields", nargs='+')
    args = args_parser.parse_args()

    organisation = args.output_folder_organisation.replace('#', '').split('/')

    # If incoming_dataset is PPMI, force use of ppmi_xml_extension
    if args.incoming_dataset.upper() == 'PPMI':
        logging.info("Enabling ppmi_xml_extension...")
        args.ppmi_xml_extension = True

    # If excluded_fields is not defined, setup to default values
    if not args.excluded_fields:
        args.excluded_fields = []
        # If ppmi_xml_extension is enabled, exclude some default fields
        if args.ppmi_xml_extension:
            logging.info("Using ppmi_xml_extension default...")
            args.excluded_fields = list(ppmi_xml_extension.MAPPING.keys())

    if args.type.upper() in ['DICOM', 'DCM']:
        dicom_organizer.organize_dicom(
            args.input_folder, args.output_folder, organisation, args.excluded_fields, args.ppmi_xml_extension,
            args.unknown_value)
    elif args.type.upper() in ['NIFTI', 'NII']:
        nifti_organizer.organize_nifti(args.incoming_dataset, args.input_folder, args.output_folder, organisation)


if __name__ == '__main__':
    main()

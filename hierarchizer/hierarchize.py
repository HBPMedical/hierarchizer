#!/usr/bin/env python3.5

import argparse
import logging
import os
import sys

from os.path import join
from os import makedirs

from hierarchizer import ppmi_xml_extension
from hierarchizer import dicom_organizer
from hierarchizer import nifti_organizer

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(join(SCRIPT_DIR, PACKAGE_PARENT)))


######################################################################################################################
# DEFAULT SETTINGS
######################################################################################################################

DEFAULT_TYPES = {'CLM': 'NIFTI', 'EDSD': 'NIFTI', 'PPMI': 'DICOM', 'ADNI': 'NIFTI'}
DEFAULT_ORGANISATION = '#PatientID/#StudyID/#SeriesDescription/#SeriesNumber'
DEFAULT_UNKNOWN_VALUE = 'unknown'


######################################################################################################################
# DEFAULT SETTINGS
######################################################################################################################

def main():
    logging.basicConfig(level=logging.INFO)

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("input_folder")
    args_parser.add_argument("output_folder")
    args_parser.add_argument("meta_output_folder")
    args_parser.add_argument("incoming_dataset")
    args_parser.add_argument("--type", nargs='?')
    args_parser.add_argument("--output_folder_organisation", default=DEFAULT_ORGANISATION)
    args_parser.add_argument("--unknown_value", default=DEFAULT_UNKNOWN_VALUE)
    args_parser.add_argument("--ppmi_xml_extension", action='store_true')
    args_parser.add_argument("--excluded_fields", nargs='+')
    args_parser.add_argument("--allowed_field_values", nargs='+')
    args = args_parser.parse_args()

    organisation = args.output_folder_organisation.replace('#', '').split('/')

    input_folder = args.input_folder
    output_folder = args.output_folder
    meta_output_folder = args.meta_output_folder
    dataset = args.incoming_dataset.upper()
    data_type = args.type
    unknown_value = args.unknown_value
    ppmi_ext_enabled = args.ppmi_xml_extension
    excl_fields = args.excluded_fields if args.excluded_fields else []
    allowed_field_values = {}
    for v in (args.allowed_field_values if args.allowed_field_values else []):
        if '=' not in v:
            logging.error("Argument allowed_field_values: expecting a parameter of the form Key1=V1,V2,V3 found %v")
            sys.exit(1)
        field, allowed_values = v.split('=')
        allowed_field_values[field] = allowed_values.split(',')

    makedirs(output_folder, exist_ok=True)
    makedirs(meta_output_folder, exist_ok=True)

    if not data_type:
        data_type = DEFAULT_TYPES[dataset]
        logging.info("Auto-configuration : type = %s", data_type)
    data_type = data_type.upper()

    if dataset == 'PPMI':
        ppmi_ext_enabled = True
        logging.info("Auto-configuration : ppmi_xml_extension = enabled")

    if ppmi_ext_enabled:
        excl_fields.extend(list(ppmi_xml_extension.MAPPING.keys()))
        logging.info("Auto-configuration : append default PPMI excluded-fields")

    if data_type in ['DICOM', 'DCM']:
        dicom_organizer.organize_dicom(
            input_folder, output_folder, organisation, excl_fields, ppmi_ext_enabled,
            unknown_value, allowed_field_values)
    elif data_type in ['NIFTI', 'NII']:
        nifti_organizer.organize_nifti(dataset, input_folder, output_folder, organisation, meta_output_folder)


if __name__ == '__main__':
    main()

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/LREN-CHUV/hierarchizer/blob/master/LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c1e88d79ac484390b612924aedc1597b)](https://www.codacy.com/app/mirco-nasuti/hierarchizer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LREN-CHUV/hierarchizer&amp;utm_campaign=Badge_Grade) [![CHUV](https://img.shields.io/badge/CHUV-LREN-AF4C64.svg)](https://www.unil.ch/lren/en/home.html)


# Hierarchizer


## Introduction

Docker container containing Python scripts that reorganize DICOM files creating a folder hierarchy from meta-data found in DICOM files
and/or external meta-data files (e.g. XML files fro PPMI).


## Usage

Run: `docker run --rm -v <input_folder>:/input_folder -v <output_folder>:/output_folder -v <meta_output_folder>:/meta_output_folder hbpmip/hierarchizer <incoming_dataset> [options]`

where:
* <input_folder> is the folder containing the input DICOM/NIFTI files
* <output_folder> is the folder that will contain the hierarchized DICOM/NIFTI files
* <meta_output_folder> is the folder that will contain the metadata files
* <incoming_dataset> is the dataset name (e.g. CLM, EDSD, PPMI, ADNI)
* options:
  * -h, --help : show help
  * --type TYPE : Type of image files (DICOM, NIFTI)
  * --output_folder_organisation OUTPUT_FOLDER_ORGANISATION : String containing DICOM fields to use to create
  the output folder hierarchy (default='#PatientID/#StudyID/#SeriesDescription/#SeriesNumber')
  * --unknown_value UNKNOWN_VALUE : value to use if a field cannot be found (default="unknown")
  * --ppmi_xml_extension : try to use meta-data from PPMI XML files if a field cannot be found in the DICOM files
  * --excluded_fields EXCLUDED_FIELDS [EXCLUDED_FIELDS ...]


## Build

Run: `./build.sh`


## Publish

Run: `./docker_push.sh`

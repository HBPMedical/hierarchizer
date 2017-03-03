[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/LREN-CHUV/hierarchizer/blob/master/LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c1e88d79ac484390b612924aedc1597b)](https://www.codacy.com/app/mirco-nasuti/hierarchizer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LREN-CHUV/hierarchizer&amp;utm_campaign=Badge_Grade)


# Hierarchizer


## Introduction

Docker container containing Python scripts that reorganize DICOM files creating a folder hierarchy from meta-data found in DICOM files
and/or external meta-data files (e.g. XML files fro PPMI).


## Usage

Run: `docker run --rm -v <input_folder>:/input_folder -v <output_folder>:/output_folder hbpmip/hierarchizer [options]`

where:
* <input_folder> is the folder containing the input DICOM/NIFTI files
* <output_folder> is the folder that will contain the hierarchized DICOM/NIFTI files
* options:
  * -h, --help : show help
  * --dataset DATASET : Dataset code (CLM, EDSD, PPMI, ADNI)
  * --type TYPE : Type of image files (DICOM, NIFTI)
  * --attributes ATTRIBUTES [ATTRIBUTES ...] : list of DICOM fields to use as a folder hierarchy
  (default=['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber'])
  * --unknown_value UNKNOWN_VALUE : value to use if a field cannot be found (default="unknown")
  * --ppmi_xml_extension : try to use meta-data from PPMI XML files if a field cannot be found in the DICOM files
  * --excluded_fields EXCLUDED_FIELDS [EXCLUDED_FIELDS ...]


## Build

Run: `./build.sh`


## Publish

Run: `./docker_push.sh`

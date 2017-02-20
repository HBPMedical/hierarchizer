[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/LREN-CHUV/hierarchizer/blob/master/LICENSE)

# Hierarchizer

## Introduction

This is a Python script that reorganize DICOM files creating a folder hierarchy from meta-data found in DICOM files
and/or external meta-data files (e.g. XML files fro PPMI).

## Prerequisites

You need Python 3.5 or higher version.
To install the required libraries, run `pip install -r requirements.txt`.

## Usage

hierarchize.py [-h] [--attributes ATTRIBUTES [ATTRIBUTES ...]] [--unknown_value UNKNOWN_VALUE] [--ppmi_xml_extension] 
input_folder output_folder

positional arguments:
* input_folder
* output_folder

optional arguments:
  * -h, --help : show help
  * --attributes ATTRIBUTES [ATTRIBUTES ...] : list of DICOM fields to use as a folder hierarchy
  (default=['PatientID', 'StudyID', 'SeriesDescription', 'SeriesNumber'])
  * --unknown_value UNKNOWN_VALUE : value to use if a field cannot be found (default="unknown")
  * --ppmi_xml_extension : try to use meta-data from PPMI XML files if a field cannot be found in the DICOM files

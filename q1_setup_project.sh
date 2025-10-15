#!/bin/bash

# Assignment 5, Question 1: Project Setup Script
# This script creates the directory structure for the clinical trial analysis project

# TODO: Create the following directories:
#   - data/
#   - output/
#   - reports/
mkdir data 
mkdir output
mkdir reports
echo "directories generated"
# TODO: Generate the dataset
#       Run: python3 generate_data.py
#       This creates data/clinical_trial_raw.csv with 10,000 patients
python3 generate_data.py

# TODO: Save the directory structure to reports/directory_structure.txt
#       Hint: Use 'ls -la' or 'tree' command
ls -la > reports/directory_structure.txt 


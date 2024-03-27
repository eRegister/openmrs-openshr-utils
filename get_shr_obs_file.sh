#!/bin/bash

# d1=$(date -d yesterday '+%d-%m-%Y')
d2=$(date +'%d-%m-%Y')

sudo /usr/bin/rclone copy onedrive:"HIE Data"/"SHR_HTS_$d2.xlsx" /home/openmrs/openmrs-openshr-utils/SHR_data
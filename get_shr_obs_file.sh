#!/bin/bash

# d1=$(date -d yesterday '+%d-%m-%Y')
d2=$(date +'%d-%m-%Y')
#check if today is friday, saturday or sunday, if not use last week's dates
if [ $(date +%u) -lt 5 ]
then
        d2=$(date -d 'last Sunday - 2 days' '+%d-%m-%Y')


elif [ $(date +%u) -gt 5 ]
then
        d2=$(date -d 'this Friday' '+%d-%m-%Y')

fi

sudo /usr/bin/rclone copy onedrive:"HIE Data"/"SHR_HTS_$d2.xlsx" /home/openmrs/openmrs-openshr-utils/SHR_data

echo "Date = $d2"

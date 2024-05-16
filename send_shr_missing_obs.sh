#!/bin/bash
d2=$(date +'%d_%m_%Y')
d2_month=$(date +"%B")
d2_year=$(date +"%Y")
#check if today is friday, saturday or sunday, if not use last week's dates
if [ $(date +%u) -lt 5 ]
then
        d2=$(date -d 'last Sunday - 2 days' '+%d_%m_%Y')
        d2_month=$(date -d 'last Sunday - 2 days' +"%B")
        d2_year=$(date -d 'last Sunday - 2 days' +"%Y")


elif [ $(date +%u) -eq 6 ]
then
        d2=$(date -d 'yesterday' '+%d_%m_%Y')
        d2_month=$(date -d 'yesterday' +"%B")
        d2_year=$(date -d 'yesterday' +"%Y")

elif [ $(date +%u) -eq 7 ]
then
        d2=$(date -d 'yesterday - 1 days' '+%d_%m_%Y')
        d2_month=$(date -d 'yesterday - 1 days' +"%B")
        d2_year=$(date -d 'yesterday - 1 days' +"%Y")

fi


sudo /usr/bin/rclone copy /home/openmrs/openmrs-openshr-utils/data/"$1_missing_HTS_observations_$d2.xlsx" onedrive:"North eRegister Backups"/"Leribe Backups"/"$2"/"$d2_year"/"$d2_month"/"Missing Observations"

echo "Date = $d2, Year = $d2_year, Month = $d2_month"

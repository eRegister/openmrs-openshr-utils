#!/bin/bash
d2=$(date +'%d_%m_%Y')
sudo /usr/bin/rclone copy /home/openmrs/openmrs-openshr-utils/data/"$1_missing_HTS_observations_$d2.xlsx" onedrive:"North eRegister Backups"/"Leribe Backups"/"Khabo HC"/"$(date +"%Y")"/"$(date +"%B")"/"Missing Observations"

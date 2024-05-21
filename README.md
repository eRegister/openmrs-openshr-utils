# openmrs-openshr-utils
utils for monitoring HTS data streaming between eRegister and SHR

Requirements
  Clone/Copy openmrs-openshr-utils repo/folder to /home/openmrs
1.	Open file “openshr_automation_global_variables.py” inside global variables folder and change variable facility_heina value to facility’s heina and also enter facility name to facility_name variable, also change facility_onedrive_folder value to be similar to facility folder name on onedrive, and then change server_python_version_dependency_path value to match python version path i.e. if python version is 3.6 edit server_python_version_dependency_path="/home/openmrs/.local/lib/python3.6/site-packages"
2.	Make sure server host is using python3 version e.g. version 3.6 => python3 --version
3.	Installing python3 version dependencies
•	If python version >= 3.6
	If you do not have pip3 installed run => sudo apt install python3-pip
	sudo pip3 install pandas 		N.B (works every time for python3.6)
•	else if python version = 3.5
	To install pip3 do: curl https://bootstrap.pypa.io/pip/3.5/get-pip-py -o get-pip.py
	sudo python3 get-pip.py --force-reinstall
	sudo pip3 install pandas
•	sudo pip3 install openpyxl
•	sudo pip3 install requests
•	sudo pip3 install xlrd==1.2.0
4.	cd openmrs-openshr-utils
5.	send 4 shell scripts to /usr/local/bin: sudo cp send_shr_missing_obs.sh get_shr_obs_file.sh hts_rapid_export_daily.sh ART_export_daily.sh hts_rapid_export_weekly.sh /usr/local/bin/
6.	sudo chown openmrs:openmrs /usr/local/bin/*
7.	sudo chmod +x /usr/local/bin/*
8.	sudo chown –R openmrs:openmrs  ~/ openmrs-openmrs-openshr-utils
9.	In Crontab add this lines:
•	*/1 * * * * python3 /home/openmrs/openmrs-openshr-utils/main_shr_missing_obs.py >> /var/log/missing_shr_obs.log 2>&1
•	*/2 * * * * python3 /home/openmrs/openmrs-openshr-utils/main_shr_missing_patients.py >> /var/log/missing_shr_patients.log 2>&1
•	*/3 * * * * python3 /home/openmrs/openmrs-openshr-utils/main_shr_missing_ART_patients.py >> /var/log/missing_shr_ART_patients.log 2>&1

When sudo tail –f /var/log/missing_shr_obs.log has no errors and 
sudo tail –f /var/log/missing_shr_ patients.log also has no errors change scheduling to this times below

•	00 18 * * 5 python3 /home/openmrs/openmrs-openshr-utils/main_shr_missing_obs.py >> /var/log/missing_shr_obs.log 2>&1
•	00 10,16 * * * python3 /home/openmrs/openmrs-openshr-utils/main_shr_missing_patients.py >> /var/log/missing_shr_patients.log 2>&1
•	05 10,16 * * * python3 /home/openmrs/openmrs-openshr-utils/main_shr_missing_ART_patients.py >> /var/log/missing_shr_ART_patients.log 2>&1
•	00 09,15 * * 1 bash /home/openmrs/openmrs-openshr-utils/gitpull_openshr_utils.sh >> /var/log/gitpull_openshr_utils.log 2>&1





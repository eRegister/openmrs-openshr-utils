#import mysql.connector
import sys
sys.path.append('/home/openmrs')
import openshr_automation_global_variables
sys.path.append(openshr_automation_global_variables.get_server_python_version_dependency_path())
import os
import shutil
import demographics_art
import find_missing_ART_clients
import convert_demographics_excel_to_csv
import send_missing_clients
import subprocess

#edit facility_name and facility_heina to that of current facility
facility_name= openshr_automation_global_variables.get_facility_name()
facility_heina= openshr_automation_global_variables.get_facility_heina()

sql_data_file="/home/openmrs/openmrs-openshr-utils/facility_ART_daily.csv"

if os.path.exists(sql_data_file):
  os.remove(sql_data_file)
  

if subprocess.call(['sh', '/usr/local/bin/ART_export_daily.sh'])==0:
  

  if os.path.exists(sql_data_file):
    if os.stat(sql_data_file).st_size!=0:
      demographics_file_name=demographics_art.demographics(facility_name,sql_data_file,facility_heina)
      if demographics_file_name:
        if not os.path.exists("/home/openmrs/openmrs-openshr-utils/data/"):
          os.mkdir("/home/openmrs/openmrs-openshr-utils/data")
        # shutil.copy(demographics_file_name, "./data/")
        print("demographics_file done")
        filename_csv="/home/openmrs/openmrs-openshr-utils/"+facility_name+"_ARTNew.csv"
        # print(convert_demographics_excel_to_csv.convert_demographics_excel_to_csv(demographics_file_name,filename_csv))
        convert_demographics_excel_to_csv.convert_demographics_excel_to_csv(demographics_file_name,filename_csv)
        print("demographics conversion done")
        print("Finding missing Clients!! Please wait...")

        missing_csv_filename=find_missing_ART_clients.find_missing_clients(filename_csv,facility_name)
        
        print("Finding missing Clients done")
        print("Sending Missing client if any!! Please wait...")
        send_missing_clients.send_missing_clients(missing_csv_filename,facility_name)
        print("Sending missing Clients done")
        print("===========================================================================================")

      else:
        print("error creating demographics file")
    else:
      print("SQL file contains zero results from mysql")
  else:
    print("could not locate file: "+ sql_data_file)
else:
  print("error quiring DB. Please check if docker container is up or if ART_export_daily.sh is in correct location")

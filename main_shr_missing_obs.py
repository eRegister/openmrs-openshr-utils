#import mysql.connector
import sys
sys.path.append('/home/openmrs/.local/lib/python3.6/site-packages')
import os
import shutil
import demograhics
import find_missing_clients
import convert_demographics_excel_to_csv
import send_missing_clients
import subprocess
import compare_eRegister_vs_hie_data
from datetime import datetime, timedelta

#edit facility_name and facility_heina to that of current facility
facility_name= "Khabo_HC"
facility_heina= "2.25.71280592878078638113873461180761116380"

sql_data_file="facility_RAPID_HTS_weekly.csv"

if os.path.exists(sql_data_file):
  os.remove(sql_data_file)
  
if not os.path.exists("./SHR_data"):
  os.mkdir("SHR_data")

if subprocess.call(['sh', '/usr/local/bin/get_shr_obs_file.sh'])==0:
  if subprocess.call(['sh', '/usr/local/bin/hts_rapid_export_weekly.sh'])==0:
    if os.path.exists(sql_data_file) and os.stat(sql_data_file).st_size!=0:
      demographics_file_name=demograhics.demographics(facility_name,sql_data_file,facility_heina)
      if demographics_file_name:
        if not os.path.exists("./data/"):
          os.mkdir("data")
        # shutil.copy(demographics_file_name, "./data/")
        print("demographics_file done")
        filename_csv=facility_name+"_HTSNew.csv"
        # print(convert_demographics_excel_to_csv.convert_demographics_excel_to_csv(demographics_file_name,filename_csv))
        convert_demographics_excel_to_csv.convert_demographics_excel_to_csv(demographics_file_name,filename_csv)
        print("demographics conversion done")
        print("===========================================================================================")
        print("Finding missing Clients!! Please wait...")

        missing_csv_filename=find_missing_clients.find_missing_clients(filename_csv,facility_name)
        
        print("Finding missing Clients done")
        print("===========================================================================================")
        print("Sending Missing client if any!! Please wait...")
        send_missing_clients.send_missing_clients(missing_csv_filename,facility_name)
        print("Sending missing Clients done")
        print("===========================================================================================")

        today = datetime.today()
        yesterday = today - timedelta(days=1)
        print(datetime.today().strftime('%d-%m-%Y'))
        # hie_data= "SHR_data/SHR_HTS_"+yesterday.strftime('%d-%m-%Y')+".xlsx"
        hie_data= "/home/openmrs/openmrs-openshr-utils/SHR_data/SHR_HTS_"+datetime.today().strftime('%d-%m-%Y')+".xlsx"
        print("SHR file :"+hie_data)
        if os.path.exists(hie_data):
          print("Comparing SHR obs with eRegister obs...")
          compare_eRegister_vs_hie_data.compare_eregister_vs_hie_data(demographics_file_name, hie_data,facility_name)
          print("Comparing SHR obs with eRegister obs done")
          if subprocess.call(['sh', '/usr/local/bin/send_shr_missing_obs.sh',facility_name])==0:
            print("missing observation file has been uploaded to onedrive")
          else:
            print("Error...missing observation file has has failed to be uploaded to onedrive")
        else:
          print("Could not find SHR obs file from onedrive")
      else:
        print("error creating demographics file")
    else:
      print("could not locate file: "+ sql_data_file+" Or file contains zero results from mysql")
  else:
    print("error fetching SHR_data file...Please internet connection or make sure your able to get onedrive using rclone!")

from openempi_session import Openempi_session
from helper import get_patients_from_csv
from helper import write_data_to_csv

def send_missing_clients(missing_csv_filename,facility_name):
    filename = missing_csv_filename
    openempi_session = Openempi_session()
    patients = get_patients_from_csv(filename)
    sent_patients = []
    failed_patients = []
    sent_patients_count=0
    failed_patients_count=0
    for patient in patients:
        if(patient.send_to_openempi(openempi_session)):
            sent_patients.append(patient)
            sent_patients_count+=1
        else:
            failed_patients.append(patient)
            failed_patients_count+=1
        
    print("=================Sent Patients (Count :"+str(sent_patients_count)+")=================\n")
    for patient in sent_patients:
        print(patient.givenName+" "+patient.familyName+"\n")

    print("=================Failed Patients (Count :"+str(failed_patients_count)+")=================\n")
    for patient in failed_patients:
        print(patient.givenName+" "+patient.familyName+"\n")

    write_data_to_csv("/home/openmrs/openmrs-openshr-utils/"+facility_name+"_sent_patients.csv", sent_patients)
    write_data_to_csv("/home/openmrs/openmrs-openshr-utils/"+facility_name+"_failed_patients.csv", failed_patients)


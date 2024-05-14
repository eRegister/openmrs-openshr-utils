#!/bin/bash

#last week  friday
d1=$(date -d 'last Sunday - 8 days' '+%Y-%m-%d')
d2=$(date -d 'last Sunday - 1 days' '+%Y-%m-%d')

#check if today is friday, saturday or sunday, if not use last week's dates
if [ $(date +%u) -eq 5 ]
then
        d1=$(date -d "6 days ago" '+%Y-%m-%d')
        d2=$(date -d "tomorrow" "+%Y-%m-%d")

elif [ $(date +%u) -eq 6 ]
then
        d1=$(date -d "7 days ago" '+%Y-%m-%d')
        d2=$(date +%Y-%m-%d)

elif [ $(date +%u) -eq 7 ]
then
        d1=$(date -d "8 days ago" '+%Y-%m-%d')
        d2=$(date -d "yesterday" "+%Y-%m-%d")
fi


a='"'
docker exec bahmni_docker_emr-service_1 rm /var/lib/mysql-files/facility_RAPID_HTS_weekly.csv

docker exec -i bahmni_docker_emr-service_1 /usr/bin/mysql -u root --password=P@ssw0rd openmrs -e "select distinct patient_identifier.identifier, person_name.given_name, 
person_name.family_name,pa.city_village as address1,pa.address2 as address2,pa.state_province as city,person.birthdate as dateOfBirth,pc.value as phoneNumber,
ni.identifier as nationalID,person.gender AS gender,pn.middle_name as mothersMaidenName,person_name.family_name2,ts.value as motherName,msc.value as maritalStatusCode from obs o 
INNER JOIN patient ON o.person_id = patient.patient_id AND o.concept_id = 2165 AND CAST(o.obs_datetime AS DATE) >= CAST('$d1' AS DATE) AND 
CAST(o.obs_datetime AS DATE) <= CAST('$d2' AS DATE) AND patient.voided = 0 AND o.voided = 0 INNER JOIN person_name pn on o.person_id = pn.person_id and pn.voided=0 
INNER JOIN person ON person.person_id = patient.patient_id AND person.voided = 0 left JOIN person_address pa on o.person_id = pa.person_id left JOIN 
person_attribute pc on o.person_id=pc.person_id and pc.person_attribute_type_id = 26 left JOIN person_attribute msc on o.person_id=msc.person_id and 
msc.person_attribute_type_id=28 left JOIN person_attribute ts on o.person_id = ts.person_id and ts.person_attribute_type_id =17 left JOIN 
patient_identifier ni on o.person_id = ni.patient_id and ni.identifier_type=4 INNER JOIN location l on o.location_id = l.location_id  and l.retired=0
INNER JOIN person_name ON person.person_id = person_name.person_id AND person_name.preferred = 1 INNER JOIN patient_identifier ON 
patient_identifier.patient_id = person.person_id AND patient_identifier.identifier_type = 3 AND patient_identifier.preferred=1 
INTO OUTFILE '/var/lib/mysql-files/facility_RAPID_HTS_weekly.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '$a' LINES TERMINATED BY '\n'"

docker cp bahmni_docker_emr-service_1:/var/lib/mysql-files/facility_RAPID_HTS_weekly.csv /home/openmrs/openmrs-openshr-utils

echo "$d1 - $d2"

import requests
import json
import re

iq_user = 'admin'
iq_password = 'password'
iq_server_url = 'http://localhost:8070'

#let's get the applications to check for names
#Check https://help.sonatype.com/iqserver/automating/rest-apis/application-rest-apis---v2 for more details on
request_response = requests.get(iq_server_url + '/api/v2/applications',auth=(iq_user, iq_password))
response_json = request_response.json()
#print (response_json)
iq_applications = response_json['applications']
for iq_application in iq_applications:
    iq_app_id = iq_application["publicId"]
    iq_app_name = iq_application["name"]
    #print iq_app_name
    reg_result = re.findall('.RC', iq_app_name,re.IGNORECASE)
    #print reg_result
    if (len(reg_result) > 0):
        print ("we would delete " + iq_app_name)
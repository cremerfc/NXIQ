Need to install requests package for python
import requests
import json

# Set the request parameters
iq_url = 'http://localhost:8070/api/v2/organizations'
sn_url = 'https://dev66887.service-now.com/api/now/table/x_77303_iq_sever_d_iq_organization'

# User credentials
iq_user = 'admin'
iq_pwd = 'password'
sn_user = 'admin'
sn_pwd = 'S0n@type'

# Set proper headers
iq_headers = {"Content-Type":"application/json","Accept":"application/json"}

# First, let's get the organizations from IQ Server

resp = requests.get(iq_url, auth=(iq_user, iq_pwd), headers=iq_headers)


# Do the HTTP request
#response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"organizationid\":\"123\",\"organizationname\":\"OrgName\"}")

# Check for HTTP codes other than 200
if resp.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# resp.content

organizations = resp.json()['organizations']

#print (str(organnizatios))
for iq_app in organizations:
    org_name = str(iq_app['name'])
    org_id = str(iq_app['id'])
    #add organizations to SN
    sn_headers = {"Content-Type":"application/json"}
    r_body = '{"organizationid":"' + org_id + '", "organizationname": "' + org_name + '"}'
    data_opts = "{\"organizationid\":\""+ org_id +"\",\"organizationname\":\"" + org_name +"\"}"
    
    #print r_body 
    sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
    print sn_response.content

# Decode the JSON response into a dictionary and use the data
#data = response.json()
#print(data)#
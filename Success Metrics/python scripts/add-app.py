import requests

#first get the applications defined in IQ
iq_url = 'http://localhost:8070/api/v2/applications'
iq_user = 'admin'
iq_pwd = 'password'

#SNOW credentials

sn_user = 'admin'
sn_pwd = 'S0n@type'

iq_headers = {"Content-Type":"application/json","Accept":"application/json"}

resp = requests.get(iq_url, auth=(iq_user, iq_pwd), headers=iq_headers)

iq_apps = resp.json()['applications']

#let's go through them and get the ORG ID in IQ
for iq_app  in iq_apps:
    app_org_id = str(iq_app['organizationId'])
    app_name = str(iq_app['name'])
    app_id = str(iq_app['id'])

    print (str(app_org_id))
    #now that we have the ORG ID for the current app, we are going to use that value to query SNOW for a matching record 
    sn_url = 'https://dev66887.service-now.com/api/now/table/x_77303_iq_sever_d_iq_organization?sysparm_query=organizationid%3D'+ app_org_id +'&sysparm_fields=sys_id&sysparm_limit=1'
    sn_headers = {"Content-Type":"application/json"}
    sn_resp = requests.get(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers)
    sn_resp_json = sn_resp.json()
    #we need the sys_id (SN internal ID of record) to set the relationship between application and organization
    sn_sys_id = sn_resp_json["result"][0]["sys_id"]
    #rest sn_url
    sn_url = 'https://dev66887.service-now.com/api/now/table/x_77303_iq_sever_d_iq_application'
    data_opts = "{\"applicationid\":\"" + app_id + "\",\"applicationname\":\"" + app_name+ "\",\"organization\":\"" + sn_sys_id + "\"}"
    sn_response = requests.post(sn_url, auth=(sn_user, sn_pwd), headers=sn_headers ,data=data_opts)
    print sn_response.content



    #print (str(sn_sys_id))



#let's submit the record
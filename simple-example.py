import requests
import json


r_body = {"timePeriod": "WEEK","firstTimePeriod": "2018-W35","lastTimePeriod": "2018-W35"}

iq_url = 'http://localhost:8070/api/v2/reports/metrics'


resp = requests.post( iq_url, auth=('Admin','password') ,json=r_body, headers={'Content-Type':'application/json', 'Accept':'application/json'})

#debug - print the raw response
print resp.content

for iq_app in resp.json():
    print (iq_app['applicationName'] + ', At the end of the current period there are (' + str(iq_app['aggregations'][0]['timePeriodStart']) + ')' + str(iq_app['aggregations'][0]['openCountsAtTimePeriodEnd']['SECURITY']['CRITICAL']) + ' open scritical violations')
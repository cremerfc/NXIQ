from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/',methods=['POST'])

def mainDef():
    #Let's get the JSON Payload
    data = json.loads(request.data)
    content = request.get_json()
    #Define Some Variables we'll need

    #The Evaluation Date
    evaluationDate = content['applicationEvaluation']['evaluationDate']
    #get the Application Name and id (id will be used with the remediation API)
    appName = content['application']['name']
    appID = content['application']['id']

    #Get the Policy Violations
    policyAlerts = content['policyAlerts']
    #Get a count of policy violations
    violationCount = len(policyAlerts)

    print "An Application Scan Took Place at " + str(evaluationDate) + " for Application " + appName
    print "There were " + str(violationCount) + " violations. They are:\n"

    #define counter since Python does not appear to have something built in
    alertIndex = 0
    #loop through the policy alerts (i.e., policy violations)

    for policyAlert in policyAlerts:
        policyName = policyAlerts[alertIndex]['policyName']
        policyID = policyAlerts[alertIndex]['policyId']
        threatLevel = policyAlerts[alertIndex]['threatLevel']
        compHash = policyAlerts[alertIndex]['componentFacts'][0]['hash']
        print policyName + " - Threat Level: " + str(threatLevel) + "\n"
        print "The following component was implicated: " + policyAlerts[alertIndex]['componentFacts'][0]['displayName'] + "\n"
        print "for the following reasons:"
        conditions = policyAlerts[alertIndex]['componentFacts'][0]['constraintFacts'][0]['satisfiedConditions']
        
        for condition in conditions:
            print condition['reason']
        #now we want to find if there is an 'upgradeable version'
        #In order to use the Remediation API we need the full component identifier but the webhook only gives us the hash and the concatenated name.
        # We'll use the Component Details API to get the coordinates
        #curl -u admin:admin123 -X POST -H "Content-Type: application/json" -d '{"components":[{"hash": "4dfca3975be3c1a98eac"}]}' 'http://localhost:8070/api/v2/components/details'
        iqUser = 'Admin'
        iqPassword = 'password'
        compDetResp = requests.post('http://localhost:8070/api/v2/components/details',headers={"Content-Type" : "application/json"},data='{"components":[{"hash": "'+ compHash +'"}]}',auth=(iqUser, iqPassword))
        compDetRespJson = compDetResp.json()


        #To help debug/troubleshoot, uncomment below to see the component identifier details
        #print compDetRespJson['componentDetails'][0]['component']['componentIdentifier']

        #we are going to deconstruct the component identifier JSON block to determine format, which will determine how we send the info..

        compFormat = compDetRespJson['componentDetails'][0]['component']['componentIdentifier']['format']
        #print compFormat
        if (compFormat=='maven'):
            #Let's build the data JSON that contains he Maven Coordinates
            #for better readability, let's define variables and assign value
            artifactId = compDetRespJson['componentDetails'][0]['component']['componentIdentifier']['coordinates']['artifactId']
            groupId = compDetRespJson['componentDetails'][0]['component']['componentIdentifier']['coordinates']['groupId']
            version = compDetRespJson['componentDetails'][0]['component']['componentIdentifier']['coordinates']['version']
            extension = compDetRespJson['componentDetails'][0]['component']['componentIdentifier']['coordinates']['extension']
            #'{"componentIdentifier": {"format":"maven","coordinates": {"artifactId":"tomcat-util","extension":"jar","groupId":"tomcat","version":"5.5.23"}}}'
            reqData = '{"componentIdentifier": {"format":"maven","coordinates": {"artifactId":"' + artifactId + '","extension":"' + extension + '","groupId":"' + groupId + '","version":"' + version +'", "classifier":""}}}'
            remAPIResp = requests.post('http://localhost:8070/api/v2/components/remediation/application/' + appID,headers={"Content-Type" : "application/json"},data=reqData,auth=(iqUser, iqPassword))
            remAPIRespJSON = remAPIResp.json()
            #print str(remAPIRespJSON['remediation']['versionChanges'])
            #if there isn't a valid version to upgrade to, the 'versionChanges' array will be empty.
            if (len(remAPIRespJSON['remediation']['versionChanges']) == 0 ):
                print "There is no version to upgrade to"
            else:
                print "The next version to upgrade is " + str(remAPIRespJSON['remediation']['versionChanges'][0]['data']['component']['componentIdentifier']['coordinates']['version'])
                print "............................................ \n"
            #
     
       # remAPIResp = requests.post('http://localhost:8070/api/v2/components/remediation/organization/' + orgID,headers={"Content-Type" : "application/json"},data='{"componentIdentifier":'+ str(compDetRespJson['componentDetails'][0]['component']['componentIdentifier']) +'}',auth=(iqUser, iqPassword))
    
        alertIndex += 1
    
    return "OK"

if __name__ == '__main__':
   app.run()
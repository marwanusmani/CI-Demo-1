import requests
import sys
import imp
import traceback
import subprocess
import os
from os import listdir
from os.path import isfile, join
from requests.utils import quote
import json
from dotenv import load_dotenv

# from kivy.graphics import Color

dotenv_path = '../script.env'
load_dotenv(dotenv_path)

apiEntityId = os.getenv('apiEntityId')
authToken = os.getenv('auth-key')
gitUser = os.getenv('git-user')
gitToken = os.getenv('git-token')
apiKey = os.getenv('apiKey')
branch = os.getenv('branch')

repoUrl = ""
template = ""
sdk = ""

failed = []
failed_gitDeployment = ""

def deleteContent(pfile):
  pfile.seek(0)
  pfile.truncate()

def run(mypath="."):  
  print("Template/Language:  ", template)
  print("current api description:  ", apiKey)

  if(template == "java_eclipse_jre_lib" or template == "JAVA_ECLIPSE_JRE_LIB"):
    repoUrl = os.getenv('java-github')
    print("Current repository:  ", repoUrl)
  elif(template == "angular_javascript_lib" or template == "ANGULAR_JAVASCRIPT_LIB"):
    repoUrl = os.getenv('angular-github') 
    print("Current repository:  ", repoUrl)
  else:
    return

  sdkUrl = "https://www.apimatic.io/api/codegen?apiKey=" + apiKey + "&template=" + template
  try:
    sdkPath = requests.get(sdkUrl)
    sdk = "https://www.apimatic.io" + sdkPath.text
  except Exception as e:
    print(e)

  print("Generated Sdk: ", sdk)

  currentIteration = "Github Deployment for " + template
  print(currentIteration)

  reqUrl = "https://gitpushr.apimatic.io/v1/git/pushnow"

  _header = {
    'Content-Type': "application/json", 
    'Accept': "application/json",
    'x-username' : gitUser,
    'x-password' : gitToken
  }


  _body = {
    "email" : "test@test.com",
    "name" : "farhan",
    "branch" : "master",
    "message" : "generated updated sdk",
    "extractZip" : bool('true'),
    "fileInfo" : {
        "url" : sdk
    },
    "repoUrl" : repoUrl
  }

  #reqUrl = append_url_with_query_parameters(url, _query_parameters)
  try:      
    r = requests.post(reqUrl, headers= _header, data=json.dumps(_body))
    print(r.status_code)
    print(r.text)
    data = json.loads(r.text)
    if(r.status_code != 200):
      failed.append("repository: " + repository + "\nTemplate: " + template + "\nStatus_Code: " + str(r.status_code) + "\nMessage: " + r.text)
      failed.append("\r\n ========================================================\r\n")
    elif(data['success'] != True):
      failed.append("repository: " + repository + "\nTemplate: " + template + "\nStatus_Code: " + str(r.status_code) + "\nMessage: " + r.text)
      failed.append("\r\n ========================================================\r\n")
  except Exception as e:
      print(e)

  try:
    # f_failed = open(join(mypath,"_failed.txt"), "w")
    for line in failed:
      failed_gitDeployment.write(line)
    failed_gitDeployment.close()

  except Exception as e:
    print(e)

if len(sys.argv) > 2:
  if(sys.argv[1]):
    # run(sys.argv[1])
    print("Current Directory: " + sys.argv[1])
    # apiKey = sys.argv[1]
    template = sys.argv[2]
    # repoUrl = sys.argv[3] 
    run(sys.argv[1])
  else:
    print("invalid directory path provided")
else:
  print("no directory provided. running in current directory")
  if len(sys.argv) > 1:
    if(sys.argv[1]):
      # apiKey = sys.argv[1]
      template = sys.argv[1]
      # repoUrl = sys.argv[3]  
      failed_gitDeployment = open('gitDeployment.txt', 'w')
      deleteContent(failed_gitDeployment)
      
      run()
  else:
    #run()
    print("invalid directory path provided")

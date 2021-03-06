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

failed = []
failed_portal = ""

def deleteContent(pfile):
  pfile.seek(0)
  pfile.truncate()

def run(mypath="."):
  print("Updating Hosted portal...")

  reqUrl = "https://www.apimatic.io/api/api-entities/" + apiEntityId + "/hosted-api-docs"

  _header = {
    'Content-Type': "application/json", 
    'Accept': "application/json",
    'Authorization' : "X-Auth-Key " + authToken
  }

  _body = {
  }

  #reqUrl = append_url_with_query_parameters(url, _query_parameters)
  try:      
    r = requests.put(reqUrl, headers= _header, data=json.dumps(_body))
    print(r.status_code)
    print(r.text)
    if(r.status_code != 204):
      failed.append("Status_Code: " + str(r.status_code) + "\nMessage: " + r.text)
      failed.append("\r\n ========================================================\r\n")
    else:
      print("Hosted Portal updated successfully")

  except Exception as e:
      print(e)

  try:
    # f_failed = open(join(mypath,"_failed.txt"), "w")
    for line in failed:
      failed_portal.write(line)
    failed_portal.close()

  except Exception as e:
    print(e)

if len(sys.argv) > 1:
  if(sys.argv[1]):
    # run(sys.argv[1])
    print("Current Directory: " + sys.argv[1])
    #apiEntityId = sys.argv[2]
    run(sys.argv[1])
  else:
    print("invalid directory path provided")
else:
  print("no directory provided. running in current directory")
  failed_portal = open('portal.txt', 'w')
  deleteContent(failed_portal)
  run()

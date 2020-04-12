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
failed_import = ""
apiDescription = "../calculator.json"

def deleteContent(pfile):
  pfile.seek(0)
  pfile.truncate()

def run(mypath="."):
  
  print("Current file:  ", apiDescription)
  
  fileName = os.path.basename(apiDescription)
  print(fileName)	
  currentIteration = "Importing api for id " + apiEntityId
  print(currentIteration)

  reqUrl = "https://www.apimatic.io/api/api-entities/" + apiEntityId


  _header = {
    'Authorization' : "X-Auth-Key " + authToken
  }

  multipart_form_data = {
        'image': (fileName, open(apiDescription, 'rb'))
  }

  try:      
    r = requests.put(reqUrl, headers= _header, files = multipart_form_data)
    print(r.status_code)
    print(r.text)
    if(r.status_code != 204):
      failed.append("Status_Code: " + str(r.status_code) + "\nMessage: " + r.text)
      failed.append("\r\n ========================================================\r\n")
    else:
      print("Description imported successfully")
  except Exception as e:
      print(e)

  try:
    # f_failed = open(join(mypath,"_failed.txt"), "w")
    for line in failed:
      failed_import.write(line)
    failed_import.close()

  except Exception as e:
    print(e)

if len(sys.argv) > 1:
  if(sys.argv[1]):
    # run(sys.argv[1])
    print("Current Directory: " + sys.argv[1])
    run(sys.argv[1])
  else:
    print("invalid directory path provided")
else:
  print("no directory provided. running in current directory")
  failed_import = open('import.txt', 'w')
  deleteContent(failed_import)
  run()

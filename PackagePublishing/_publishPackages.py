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
import string
import random

dotenv_path = '../script.env'
versionFile = '../version.txt'
load_dotenv(dotenv_path)

apiEntityId = os.getenv('apiEntityId')
authToken = os.getenv('auth-key')
language = os.getenv('langauge')
repository = os.getenv('packageRepository')
packageName = os.getenv('packageName')
version = ""
version_file = ""
detectedVersion = ""

failed = []
failed_packagePublish = ""

def id_generator(size=5, chars=string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def deleteContent(pfile):
  pfile.seek(0)
  pfile.truncate()

def run(mypath="."):

  #get version from pypi
  pypiReqUrl = "https://pypi.org/pypi/"+ packageName +"/json"
  try:
    pypiRes = requests.get(pypiReqUrl)
    print(pypiRes)
    if(pypiRes.status_code == 200):
      versionDict = pypiRes.json()['releases'].keys()
      versionDict = list(versionDict)
      versionDict.sort(key=lambda s: list(map(int, s.split('.'))))
      print(versionDict)
      lastVersion = versionDict[-1]
      splitVerion = parts = lastVersion.split(".")
      currentVersion = splitVerion[2]
      # print(currentVersion)
      detectedVersion = str(splitVerion[0]) + "." + str(splitVerion[1]) + "." + str(int(currentVersion) + 1)
      print(detectedVersion)
    else:
      detectedVersion = "1.0.0"
      currentVersion = "0"
      print(detectedVersion)
  except Exception as e:
    print(e)

  version_file = open(versionFile, "w")
  # currentVersion = version_file.readline()
  # cur_v = int(currentVersion)
  # cur_v = cur_v + 1
  # currentVersion = id_generator()

  version = detectedVersion
  deleteContent(version_file)
  # version_file.write(str(cur_v))
  version_file.write(str(detectedVersion))
  version_file.close()

  print("Current repository:  ", repository)
  currentIteration = "Publishing package for " + language
  print(currentIteration)

  reqUrl = "https://www.apimatic.io/api/api-entities/" + apiEntityId + "/published-packages"

  _header = {
    'Content-Type': "application/json", 
    'Accept': "application/json",
    'Authorization' : "X-Auth-Key " + authToken
  }

  _body = {
    "packageName" : packageName,
    "version" : version,
    "packageRepository" : repository,
    "template" : language ,
    "additionalDeploymentInformation": {}
  }

  #reqUrl = append_url_with_query_parameters(url, _query_parameters)
  try:      
    r = requests.post(reqUrl, headers= _header, data=json.dumps(_body))
    print(r.status_code)
    print(r.text)
    if(r.status_code != 201):
      failed.append("repository: " + repository + "\nTemplate: " + language + "\nStatus_Code: " + str(r.status_code) + "\nMessage: " + r.text)
      failed.append("\r\n ========================================================\r\n")
  except Exception as e:
      print(e)

  try:
    # f_failed = open(join(mypath,"_failed.txt"), "w")
    for line in failed:
      failed_packagePublish.write(line)
    failed_packagePublish.close()

  except Exception as e:
    print(e)

if len(sys.argv) > 1:
  if(sys.argv[1]):
    print("Current Directory: " + sys.argv[1])
    # packageName = sys.argv[2]
    # apiEntityId = sys.argv[3]
    run(sys.argv[1])
  else:
    print("invalid directory path provided")
else:
  print("no directory provided. running in current directory")
  failed_packagePublish = open('packagePublish.txt', 'w')
  deleteContent(failed_packagePublish)    
  run()

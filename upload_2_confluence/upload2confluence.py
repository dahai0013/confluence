#!/usr/bin/python3

import datetime
import json
import requests
from requests.auth import HTTPBasicAuth
import yaml
import unicodedata
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()


def get_call_api(url):
    """
    call API for this url
    :param url:
    :param auth:
    :return:
    """
    # get auth
    auth = get_credential()

    headers = {
      "Accept": "application/json",
    }
    response = requests.request(
      "GET",
      url,
      headers=headers,
      auth=auth,
      verify=False
    )
    #return (response.text)
    return (json.loads(response.text))

def create_storage_value(space_key,parent_id,baseurl,title,soup):

    # POST /rest/api/content/
    url = baseurl+"content/"

    # Create the dpayload
    dpayload = {}
    #dpayload['version'] = {}
    dpayload['title'] = {}
    dpayload['type'] = {}
    dpayload['body'] = {}
    dpayload['body']['storage'] = {}
    dpayload['space'] = {}
    dpayload['space']['key'] = {}


    dpayload['title'] = title
    dpayload['type'] = "page"
    # for PUT
    #dpayload['version']['number'] = 1
    dpayload['space']['key'] = space_key
    dpayload['body']['storage']['value'] = str(soup.html)
    print("str(soup.html):",str(soup.html))
    dpayload['body']['storage']['representation'] = "storage"
    #print("dpayload :\n",dpayload['body']['storage']['value'].replace(r'ï»¿<html','<hmtl'))
    print("dpayload :\n",dpayload)

    # log this message
    now = datetime.datetime.now()
    str_to_log = "\n\n" + str(now) + \
                 "\njson format HTTP REQUEST:\n" + \
                 json.dumps(dpayload) + \
                 "\nWeb url of the page:\n" + \
                 url
    log_message(str_to_log)

    response = post_call_api(url,dpayload)
    #print(response)

def post_call_api(url,dpayload):

    payload = json.dumps(dpayload)
    print ("\nPayload :",payload)
    # get auth
    auth = get_credential()

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    }
    response = requests.request(
      "POST",
      url,
      data=payload,
      auth=auth,
      headers=headers,
      verify=False
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    return(response)

def log_message(str_to_log):
   # save into a file the future changes
   now = datetime.datetime.now()
   filename = "change_log/"+str(now.strftime("%Y_%m_%d"))+".log"
   file = open(filename,"a")
   file.write(str_to_log)
   file.close()

def get_credential():
    credentialfilename = r"../credential.yaml"
    diccredential = yaml.load(open(credentialfilename))
    urlbase = diccredential['urlbase']
    auth = HTTPBasicAuth(diccredential['username'], diccredential['key'])
    return (auth)

def log_message(str_to_log):
   # save into a file the future changes
   now = datetime.datetime.now()
   filename = "change_log/"+str(now.strftime("%Y_%m_%d"))+".log"
   file = open(filename,"a")
   file.write(str_to_log)
   file.close()

def read_webpage_file(path,filename):
    #
    # pathfilename = path+filename
    # file = open(pathfilename, "r")
    # htmlcontent = file.read()
    # #print(htmlcontent)
    # file.close()
    response = open(path+filename, 'r')
    # Parse the html file
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    #print(str(soup))
    return (soup)

def main():
    print("Started")
    dspace_content = {}

    baseurl = r'https://thefreetelecomuni.atlassian.net/wiki/rest/api/'

    space_key = "TEST"
    space_url = baseurl+'space/'+space_key
    print("\n Space URL",space_url)

    # get the dspace content
    print("Space content")
    dspace_content = get_call_api(space_url)

    # read yaml_file and extract parent
    parent_id = 15302657
    title = "Ixia Tester"
    path = r"C:\Users\jkriker\Google Drive\FTUwebsite\O0O000OOO00O\migrate framed to unframed/cleaned/"
    filename = "IxiaTester.html"
    soup = read_webpage_file(path,filename)

    # check if parent exist

    # try to write
    print ("Will write to file")
    #print(dspace_content['key'], parent_id, baseurl)
    response = create_storage_value(dspace_content['key'], parent_id, baseurl,title,soup)
    print(response)

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
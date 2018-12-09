#!/usr/bin/python3

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
import datetime
import re
import yaml

urllib3.disable_warnings()

#urlbase = "https://thefreetelecomuni.atlassian.net/wiki/rest/api"
#space_url = urlbase+"/space"
#auth = HTTPBasicAuth("dahai0013@googlemail.com", "L6FNjAfG77iYnXRNZxUv50F3")
spacelist = ['JA', 'JO', 'JIO', 'JUN', 'JS', 'JS2', 'LIN', 'NS7', 'NN', 'RP']
#search_string = r'?cql=(text ~ "http://www.freetelecomuni.co.uk/juniper/lib/header1.jpg")'
search_string = r'?cql=(text ~ "http://www.freetelecomuni.co.uk/O0O000OOO00O/latest_SDN_HTML/lib/header1.jpg")'

#future ::    def call_api(method,url,auth,payload)
def call_api (url,auth):
   """
   call API for this url
   :param url:
   :param auth:
   :return:
   """
   headers = {
      "Accept": "application/json"
   }
   response = requests.request(
      "GET",
      url,
      headers=headers,
      auth=auth,
      verify=False
   )
   return (json.loads(response.text))


def get_content_search (urlbase,search_string,auth):
   """
   do a CQL search and return all the pages id( list )
   :param urlbase:
   :param search_string:
   :param auth:
   :return:
   """
   listpageid = []
   url = urlbase+"/content/search"+search_string
   # call one page at the time
   dicdata = call_api(url, auth)
   #
   for pagekey in range(0, len(dicdata['results'])):
      listpageid.append(dicdata['results'][pagekey]['id'])
   return(listpageid)


def get_content_version(listpageid,urlbase,auth):
   dictpageid = {}
   url = urlbase + "/content/" + str(listpageid)
   #print(url)
   # call the Confluence API
   dicdata = call_api(url, auth)
   dictpageid['id'] = listpageid
   dictpageid['title'] = dicdata['title']
   dictpageid['version'] = dicdata['version']['number']
   #print ("id:",dictpageid['id']," and  Version number:",dictpageid['version'])
   return(dictpageid)


def get_content_storage(dictpageid,urlbase,auth):
   dict = {}

   # call Confluence API to get space key
   dict['space'] = {}
   url = urlbase + "/content/" + str(dictpageid['id'])
   dicdata = call_api(url, auth)
   #print ("dicdata for the space key:",dicdata)
   dict['space']['key'] = dicdata['space']['key']
   #print("space key:",dict['space']['key'],"\n")
   # for later in the script
   space_title= dicdata['space']['name']
   # web page, just for debug
   web_url = "https://thefreetelecomuni.atlassian.net/wiki/spaces/"+str(dict['space']['key'])+"/pages/"+dicdata['id']
   #print("WEB url of the page:\n",web_url,"\n")

   dicdata = {}
   # call Confluence API to get content storage
   url = urlbase+"/content/"+str(dictpageid['id'])+"/?expand=body.storage"
   dicdata = call_api(url, auth)
   #print ("dicdata:",dicdata)
   #extract storage value ( webpage )
   strresult = dicdata['body']['storage']['value']
   #print("Storage value Before: ",strresult)
   # Substitution Option1:
   # Original:   "<p><a href=\"http://freetelecomuni.co.uk\"><ac:image><ri:url ri:value=\"http://www.freetelecomuni.co.uk/juniper/lib/header1.jpg\" />"
   # target:    "<p><ac:image><ri:attachment ri:filename=\"headerFTU.jpg\" ri:version-at-save=\"2\">"

   new_string = r'<p><ac:image><ri:attachment ri:filename="headerFTU.jpg" ri:version-at-save="2"><ri:page ri:content-title="'+space_title+r'" ri:version-at-save="1" /></ri:attachment></ac:image></p>'
   #print("new_string:\nS",new_string,"\n")

   # match 1
   #reg_string1 = r'\A^.*jpg\"\s\/></ac:image></a></p>'
   reg_string1 = r'\A^<p>.*\s/></ac:image></a></p>'
   # match 2
   reg_string2 = r'\A^.*g\"\s/></ac:image></p>'
   # match 3
   #reg_string3 = r'\A^.*pg\\\"\s/></ac:image></code></p>'
   reg_string3 = r'\A^<p>.*\s/></ac:image></code></p>'
   updated_string = re.sub(reg_string1,new_string,strresult)
   #print(strresult)
   print("match1:\n",updated_string)
   if updated_string==strresult:
      updated_string = re.sub(reg_string2,new_string,strresult)
      print ("match2:\n", updated_string,"\n")
      if updated_string == strresult:
         updated_string = re.sub(reg_string3, new_string, strresult)
         print("match3:\n", updated_string, "\n")

   dict['version'] = {}
   dict['title'] = {}
   dict['type'] = {}
   dict['body'] = {}

   dict['body']['storage'] = {}
   dict['version']['number'] = dictpageid['version']+1
   dict['title'] = dicdata['title']
   dict['type'] = "page"
   dict['body']['storage']['value'] = updated_string
   dict['body']['storage']['representation']= "storage"
   # need to add this one
   # storage: [ value: writer.toString(), representation: "storage" ]
   #print("dict:\n",json.dumps(dict),"\n")

   # PUT /rest/api/content/
   url = urlbase+"/content/"+dicdata['id']
   #print("API url of the page:\n",url,"\n")

   # log this message
   now = datetime.datetime.now()
   str_to_log = "\n\n" + str(now) + "\nContent after:\n" + updated_string + "\njson format HTTP REQUEST:\n" + json.dumps(dict) + "\n" + "Web url of the page:\n" + web_url
   log_message(str_to_log)


   headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
   }

   payload = json.dumps(dict)

   response = requests.request(
      "PUT",
      url,
      data=payload,
      auth=auth,
      headers=headers
   )

   #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

   # print (dict)
   return(dict)


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
   #yaml.close(credentialfilename)
   return (urlbase,auth)

def main():
   listpageid = []
   listpageversion = []
   dictpageid = {}

   print("start")

   # get credential
   returntuple = get_credential()
   urlbase = returntuple[0]
   auth = returntuple[1]
   # stop here

   # get a list of all the page id matching the search
   listpageid = get_content_search (urlbase,search_string,auth)
   #for testing : for on a specifig page
   #listpageid = ['852057','852057','852057']
   print("stage1: get a list of all the page id matching the search")
   # get version from page content
   ##test single page:
   for x in range(2,len(listpageid)):
      listpageversion.append(get_content_version(listpageid[x],urlbase,auth))
   #print("stage2: get version from page content",listpageversion)
   print("stage2: get version from page content")

   # modify the string and update the page
   ##test single page:
   for x in range(2,len(listpageversion)):
      print ("page :",listpageversion[x])
      new_string = get_content_storage(listpageversion[x],urlbase,auth)
      #print ("After: \n",new_string)
      #print("stage3: modify the string and update the page")
   #
   print("La fin for the first 25")

   #print (dicimage)

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
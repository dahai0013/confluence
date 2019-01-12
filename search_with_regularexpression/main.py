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
from jlk_py_lib import jlk_modules as jlk

urllib3.disable_warnings()

def main():
   listpageid = []
   listpageversion = []
   lpageidmatchregexp = []
   dictpageid = {}
   urlbase = "https://thefreetelecomuni.atlassian.net/wiki/rest/api"
   space = "JS2"
   # space_url = urlbase+"/space"
   search_string = r'<p><ac:image><ri:attachment ri:filename=\"headerFTU.jpg\" ri:version-at-save=\"1\"><ri:page ri:space-key=\"JS2\" ri:content-title=\"Juniper Switching Home page\" ri:version-at-save=\"3\" /></ri:attachment></ac:image></p>'

   print("start")

   # get credential
   auth, username , key , urlbase = jlk.get_credential()

   # get a list of all the page id matching the search
   lpageid, response_code = jlk.get_list_id_page(urlbase,auth,space)
   print(lpageid)
   print(response_code)
   #listpageid = jlk.get_content_search (urlbase,search_string,auth)
   #for testing : for on a specifig page
   #listpageid = ['852057','852057','852057']
   #print("stage1: get a list of all the page id matching the search")

   # get pageid of page matching 
   ##test single page:
   for x in range(0,len(listpageid)):
      lpageidmatchregexp.append(jlk.get_content_search_regexp(urlbase,auth,listpageid[x],search_string))
   print("stage2: get version from page content",lpageidmatchregexp)

   #print("stage2: get version from page content." )
   # # modify the string and update the page
   # ##test single page:
   # for x in range(2,len(listpageversion)):
   #    print ("page :",listpageversion[x])
   #    new_string = get_content_storage(listpageversion[x],urlbase,auth)
   #    #print ("After: \n",new_string)
   #    #print("stage3: modify the string and update the page")
   # #
   # print("La fin for the first 25")
   #
   # #print (dicimage)

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
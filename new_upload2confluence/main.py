# Load API wrapper from library
from PythonConfluenceAPI import ConfluenceAPI
import yaml,json
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

"""
    Install module:  
        pip3 install PythonConfluenceAPI
        pip3 install future
"""

def get_credential():
    """
    Read the credentail.yaml file and export: auth,username and password
    :return: tuple auth ( base64 encoded) , username (str) and password(str)
    """
    credentialfilename = r"../credential.yaml"
    diccredential = yaml.load(open(credentialfilename))
    urlbase = diccredential['urlbase']
    auth = HTTPBasicAuth(diccredential['username'], diccredential['key'])
    return (auth,diccredential['username'], diccredential['key'])


def create_storage_value(space_key,baseurl,title,soup):
#def create_storage_value(space_key,parent_id,baseurl,title,soup):

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
    dpayload['body']['storage']['value'] = str(soup)
    #print("str(soup):",str(soup))
    dpayload['body']['storage']['representation'] = "storage"
    #print("dpayload :\n",dpayload['body']['storage']['value'].replace(r'ï»¿<html','<hmtl'))
    #print("dpayload :\n",dpayload)

    #print(type(dpayload))
    #response = (url,dpayload)
    # print(response)
    return (dpayload)


def main():
    baseurl = r'https://thefreetelecomuni.atlassian.net/wiki'
    dpage_content = {}
    print("Start:")
    # get username and password
    auth,username,key = get_credential()

    # Create API object.
    print("Create API objects")
    api = ConfluenceAPI(username,key, 'https://thefreetelecomuni.atlassian.net/wiki')

    # print space_id
    print("get space infor")
    dspace = api.get_space_information('TEST')
    space_key = dspace['key']
    space_id = dspace['id']
    #parent_id = api.get_space_information(space_key)
    #print("\nspace_key:",space_key,"\nspace_id ;",space_id)
    title = "page title 5"
    soup = "<html><body>HEllo world 5</body></html>"


    # copy webpage to confluence
    print ("Create the page content")
    #dpage_content = create_storage_value(space_key,parent_id,baseurl,title,soup)
    dpage_content = create_storage_value(space_key,baseurl,title,soup)
    print("create the page")
    decho_page = api.create_new_content(dpage_content)
    print("ID of the page created :",decho_page['id'])

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
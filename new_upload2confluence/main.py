# Load API wrapper from library
from PythonConfluenceAPI import ConfluenceAPI
import yaml
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


    response = (url,dpayload)
    #print(response)

def main():
    baseurl = r'https://thefreetelecomuni.atlassian.net/wiki'

    # get username and password
    auth,username,key = get_credential()

    # Create API object.
    api = ConfluenceAPI(username,key, 'https://thefreetelecomuni.atlassian.net/wiki')

    # print space_id
    dspace = api.get_space_information('TEST')
    space_key = int(dspace['key'])
    parent_id = api.get_space_information()
    print("\nspace_key:",space_key,"\nspace_id ;",parent_id)
    title = "page title"
    soup = "<html><body>HEllo world</body></html>"


    # copy webpage to confluence
    dpage_content = create_storage_value(space_key,parent_id,baseurl,title,soup)
    api.create_new_content(dpage_content)


if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
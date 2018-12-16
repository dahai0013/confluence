from confluence.client import Confluence
import yaml
import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings()

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

def main():
    print("Started")
    dspace_content = {}

    baseurl = r'https://thefreetelecomuni.atlassian.net/wiki/rest/api/'

    space_key = "TEST"
    space_url = baseurl+'space/'+space_key
    #print("\n Space URL",space_url)

    # get the dspace content
    #print("Space content")
    #dspace_content = get_call_api(space_url)
    #space_id = Confluence.get_spaces(self,)
    auth,username,key = get_credential()
    print(username)
    print(key)
    with Confluence('https://thefreetelecomuni.atlassian.net/wiki/rest/api/space/LIN', (username, key)) as c:
        pages = c.search('ID=1')
        #space_test = c.get_space("LIN")
        #page_x = c.get_anonymous_user()
        print("pages:",pages)
        #print(space_test)


    # # read yaml_file and extract parent
    # parent_id = 15302657
    # title = "Ixia Tester"
    # path = r"C:\Users\jkriker\Google Drive\FTUwebsite\O0O000OOO00O\migrate framed to unframed/cleaned/"
    # filename = "IxiaTester.html"
    # soup = read_webpage_file(path,filename)
    #
    # # check if parent exist
    #
    # # try to write
    # print ("Will write to file")
    # #print(dspace_content['key'], parent_id, baseurl)
    # response = create_storage_value(dspace_content['key'], parent_id, baseurl,title,soup)
    # print(response)

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
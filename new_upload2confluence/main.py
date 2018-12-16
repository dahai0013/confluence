# Load API wrapper from library
from PythonConfluenceAPI import ConfluenceAPI
import yaml
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

# get username and password
auth,username,key = get_credential()
print(username)
print(key)

# Create API object.
api = ConfluenceAPI(username,key, 'https://thefreetelecomuni.atlassian.net/wiki')

#api.getspaces

# Get latest visible content from confluence instance.
confluence_recent_data = api.get_content()

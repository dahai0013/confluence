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


def main():
    # get username and password
    auth,username,key = get_credential()

    # Create API object.
    api = ConfluenceAPI(username,key, 'https://thefreetelecomuni.atlassian.net/wiki')

    # print space content
    dspace_content = api.get_space_content('TEST')
    print(type(dspace_content))
    #print("\n\n:",dspace_content.['id'])


if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
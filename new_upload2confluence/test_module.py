# Load API wrapper from library
from PythonConfluenceAPI import ConfluenceAPI
import pyconfluence as pyco
#import yaml,json, os
#from requests.auth import HTTPBasicAuth
import urllib3
from jlk_py_lib import jlk_modules as jlk

urllib3.disable_warnings()

print("page exist:", pyco.page_exists("IT","TEST"))
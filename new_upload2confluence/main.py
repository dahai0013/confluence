# Load API wrapper from library
from PythonConfluenceAPI import ConfluenceAPI
import pyconfluence as pyco
#import yaml,json, os
#from requests.auth import HTTPBasicAuth
import urllib3
from jlk_py_lib import jlk_modules as jlk

urllib3.disable_warnings()

"""
    Install module:  
        pip3 install PythonConfluenceAPI
        pip3 install future
"""

path = r'C:\Users\jkriker\Google Drive\FTUwebsite\O0O000OOO00O\migrate framed to unframed'
urlbase = r'https://thefreetelecomuni.atlassian.net/wiki'
space_key = 'TEST'

def main():

    dpage_content = {}
    print("Start:")
    # get username and password
    auth,username,key = jlk.get_credential()

    # Create API object.
    print("Create API objects")
    api = ConfluenceAPI(username,key, 'https://thefreetelecomuni.atlassian.net/wiki')

    # print space_id
    print("get space information")

    # get list of .html files
    print("get list of .html files")
    lnewlist = jlk.get_list_file(path+'\\cleaned')
    print("### List of html files :",lnewlist)

    # will loop thru all the file in the directory
    for filename in lnewlist:
        # filename is an .html file >>> yfilename is .yaml file
        yfilename = filename.strip(".html") + '.yaml'
        dicyaml = jlk.get_yaml_to_dict(path+'\\yaml',yfilename)
        lTier = dicyaml['Tier']
        print("#### list lTier :", lTier," for the file :",filename)

        # will loop thru all the tiers in the YAML file
        for mytier in lTier:
            print("######### mytier value :",mytier," and ",lTier[mytier])
            # set all value to create an content page
            dspace = api.get_space_information(space_key)
            #space_key = dspace['key']
            space_id = dspace['id']


            # information from the yaml file
            # check if all Tier exist
            print("---- call jlk.get_content_by_title() ----")
            tier_id, response_code = jlk.get_content_by_title(urlbase,lTier[mytier],auth,space_key)
            print("### tier1_id :",tier_id," and ",response_code)
            page_id, response_code = jlk.check_page_exist_id(tier_id,auth)
            #print(response_code)
            #print("page exist:", pyco.page_exists(lTier[mytier],"TEST"))
            #print(parent_id)
            #exit()
            print("### print response code :",response_code,"\n\n")

            # if the tier does not exist >>> just need to create a page
            if (response_code == 404 ):
                #or (tier_id == 0 ):
                print("####### Code :",response_code,"'page not found',  Page does not exist and tier_id :",tier_id)
                #
                # read the file and copy
                f = open(path + '\\' + filename, "r")
                #print("html file ;",f.read())
                soup = f.read()
                dpage_content = jlk.create_storage_value(space_key, tier_id, urlbase, lTier[mytier], soup)
                print ("### dpage_content :",dpage_content)
                # create the new page
                api.create_new_content(dpage_content)
                # check the new page has been created
                tier_id, response_code = jlk.get_content_by_title(urlbase, lTier[mytier], auth)
                print("Newly create page id is:", tier_id ," and ",response_code)
                continue
            # if the page exist >>> need to look at the next tier
            if (response_code == 200) and (tier_id != 0 ):
                print("####### Code :",response_code," Page exist. And tier_id :",tier_id)
                continue
            else :
                print("did not match anything ")

        # all the tier have been created , now create the page with the last tier of the list as the parent
        print("#### title :",dicyaml['Title']," and filename :",filename.strip('.html'))
        title = dicyaml['Title']
        #page_name = filename.strip('.html')

        # read the html file
        f = open(path+'\\'+filename, "r")
        #print("html file ;",f.read())
        soup = f.read()
        #print("Soup :",soup)


    # copy webpage content
    print("Create the page content")
    #dpage_content = create_storage_value(space_key,parent_id,urlbase,title,soup)
    dpage_content = jlk.create_storage_value(space_key,tier_id,urlbase,title,soup)

    # and copy to confluence
    #print("create the page :",dpage_content)
    #decho_page = api.create_new_content(dpage_content)
    #print("ID of the page created :",decho_page['id'])

    # list all pages
    print(api.get_space_information('TEST'))

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
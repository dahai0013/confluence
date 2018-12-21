import requests
from requests.auth import HTTPBasicAuth
import sched, time, datetime
import datetime
import sqlite3
import urllib3
import yaml
from PythonConfluenceAPI import ConfluenceAPI

urllib3.disable_warnings()

# create a database
conn = sqlite3.connect('api_response_time.db')
c = conn.cursor()
now = datetime.datetime.now()
s = sched.scheduler(time.time, time.sleep)

lapi_result = []

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

def do_something(sc):
    #print("Doing stuff...")
    now = datetime.datetime.now()
    try:
        api_result = measureTime(get_space)
    except    :
        print("Something when wrong ")
        api_result = {"date":now.strftime("%Y_%m_%d"),"timestamp":now.strftime("%H:%M:%S"),"exit_code":"999"}
    dynamic_data_entry(api_result)
    s.enter(2, 1, do_something, (sc,))

def measureTime(get_space):
    #print("start measuring time")
    #start = time.clock()
    start = time.process_time()
    #print("start time :",start)
    api_result = get_space()
    #elapsed = time.clock()
    elapsed = time.process_time()
    #print("stop time :",elapsed)
    elapsed = elapsed - start
    #print("diff :",elapsed)
    api_result["lapse"] = elapsed
    return(api_result)

def get_space():
    urlbase = "https://thefreetelecomuni.atlassian.net/wiki"
    space_url = urlbase + "/rest/api/space"
    # download the attachment
    #space_url = "https://thefreetelecomuni.atlassian.net/wiki/spaces/LIN/pages/16056458/1Mpage"
    auth,username,key = get_credential()
    #print ("Auth :",auth)
    headers = {
      "Accept": "application/json"
    }

    # call confluence API
    response = requests.request(
      "GET",
      space_url,
      headers=headers,
      auth=auth,
      verify=False
    )
    now = datetime.datetime.now()
    api_result = {"date":now.strftime("%Y_%m_%d"),"timestamp":now.strftime("%H:%M:%S"),"xtimestamp":now.strftime("%H%M%S"),"exit_code":response.status_code}
    return(api_result)

def create_table():
    name_table = str(now.strftime("%Y_%m_%d"))
    longcommand = ("CREATE TABLE IF NOT EXISTS date_"+name_table+" (xtimestamp INTEGER, timestamp REAL,lapse REAL, exit_code INTEGER)")
    c.execute(longcommand)
    return(name_table)

def dynamic_data_entry(api_result):
    timestamp = api_result['timestamp']
    #print(timestamp)
    xtimestamp = int(api_result['xtimestamp'])
    #xtimestamp = str(timestamp)
    #print(xtimestamp)
    lapse = api_result['lapse']
    exit_code = api_result['exit_code']
    name_table = str(api_result['date'])
    #print("INSERT INTO date_"+name_table+" (xtimestamp, timestamp, lapse, exit_code) VALUES (%s, %s, %s, %s)" % (xtimestamp,timestamp, lapse, exit_code))
    # c for connection
    c.execute ("INSERT INTO date_"+name_table+" (xtimestamp,timestamp, lapse, exit_code) VALUES (?, ?, ?, ?)",(xtimestamp,timestamp, lapse, exit_code))
    conn.commit()

def main():
    print("Started!")
    create_table()
    # s for scheduler
    s.enter(10, 1, do_something, (s,))
    s.run()
    c.close
    conn.close()

if __name__ == "__main__":
    # 1: will strip the first argument, the script.py itself
    main()
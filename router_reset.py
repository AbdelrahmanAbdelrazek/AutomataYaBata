import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

username = 'admin'
password = '35601651'

print("Getting Login Token.")
r = requests.get("https://192.168.1.1", verify=False)
loging_token_search = "getObj(\"Frm_Logintoken\").value = "
login_token = 0
for line in r.text.splitlines():
    if loging_token_search in line:
        login_token = int(line.replace(loging_token_search, "").replace("\"", "").replace(";", ""))
        print("Found")
        break
if(r.status_code == 200):
    print("Login Token =", str(login_token)+".")
else:
    print("ERROR")
    exit()


print("Logging in.")
r = requests.post('http://192.168.1.1', headers=headers, verify=False, data = {
    'frashnum':'',
    'action':'login',
    'Frm_Logintoken':login_token,
    'Username':username,
    'Password':password
    })
if(r.status_code == 200):
    print("Login Successfully.")
else:
    print("ERROR")
    exit()


print("Getting Session Token.")
r = requests.post('http://192.168.1.1/template.gch', verify=False)
session_token_search = "var session_token = "
session_token = 0
for line in r.text.splitlines():
    if session_token_search in line:
        session_token = int(line.replace(session_token_search, "").replace("\"", "").replace(";", ""))
        break
if(session_token == 0):
    print("Failed to get session token")
    exit(1)
    
if(r.status_code == 200):
    print("Session Token =", str(session_token)+'.')
else:
    print("ERROR")
    exit()

print("Restarting Router.")
params = {
    "pid" : 1002,
    "nextpage" : "manager_dev_conf_t.gch"
}

restarting_data = {
    "IF_ACTION" : "devrestart",
    "IF_ERRORSTR": "SUCC",
    "IF_ERRORPARAM" : "SUCC",
    "IF_ERRORTYPE" : -1,
    "flag": 1,
    "_SESSION_TOKEN": session_token
}
r = requests.post("http://192.168.1.1/getpage.gch", params = params, headers=headers, verify=False, data=restarting_data )

if(r.status_code == 200):
    print("Restart request sent.")
else:
    print("ERROR")
    exit()
# r = requests.post('http://192.168.1.1', headers=headers, verify=False, data = {
#     "logout":1,
#     "_SESSION_TOKEN": session_token
#     })
htmlfile = open("html.html", "w+")
htmlfile.write(r.text)

url = "http://www.google.com"
timeout = 3
while True:
    num_tries = 3 #6 seconds
    try:
        request = requests.get(url, timeout=timeout)
        print("Waiting to disconnect from the Internet.")
        time.sleep(2)
        num_tries -= 1
        if(not num_tries):
            print("Failed to restart router.")
            print ("Exiting.")
            exit()
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Disconnected from the Internet.")
        break

code = 1024
while True:
    num_tries = 18 #3 minutes
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet.")
        print("Exiting")
        break
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Waiting for internet connection.")
        time.sleep(10)
        num_tries -= 1
        if(code != 0):
            code = os.system("nmcli c up TikTak")
            print("Failed to connect to TikTak" if code !=0 else "Connected to TikTak")
        if(not num_tries):
            print("Failed to restore internet connection.")
            print ("Exiting.")
            exit()

# r = requests.get("https://192.168.1.1/ghtml", headers=headers, verify=False)
# print(r.text)
#wlp4s0

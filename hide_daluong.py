from api_automation import *
from Connect_selenium import *
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import requests
error_profiles = []
used_uuids = set()

def get_unused_uuid(index):
    global used_uuids
    url = "http://127.0.0.1:5555/profileList?page=1&limit=10000" # get list profile 

    # Send an HTTP GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Access the "content" key in the JSON data
        uuid_list = [item["uuid"] for item in data["data"]["content"]]
        
        # Find an unused UUID at the specified index
        for i, uuid in enumerate(uuid_list):
            if uuid not in used_uuids:
                used_uuids.add(uuid)
                if i == index:
                    return uuid
    
    return None






num = list(range(57, 100+1)) # num = với thứ tự của uuid get được ở list 
       # Shuffle the list randomly



def process_chrome_profile(chrome_profile, uuid):
    if uuid:
    
        print(f'Acc {chrome_profile}')
# URL của yêu cầu POST
        try:
            
            
            remote_port = OpenProfile(uuid)
            
            print("Remote port --->  ",remote_port)
            time.sleep(5)
            driver = connect_to_debug_port(remote_port)
            
        
            
            url = "https://de.fi/login" # điền url
            
            driver = GotoUrl(driver,url)
            time.sleep(5)
            # thao tác lệnh ở đây
            
           
            url = f'http://127.0.0.1:5555/closeProfile?uuid={uuid}'
            response = requests.get(url)
           # url = "http://127.0.0.1:5555/delete-profile"
            #data = {
            #"uuid_browser": [uuid]}
        # Gửi yêu cầu DELETE
            #response = requests.delete(url, json=data)
            #print(response.text)
            # #get requets
            # GetRequest(driver) 
         
        except Exception as e:
            print("Error processing Acc", chrome_profile)
            print(str(e))
            error_profiles.append(chrome_profile)
            url = f'http://127.0.0.1:5555/closeProfile?uuid={uuid}'
            response = requests.get(url)




def TestScript():
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor: # số luồng
        for n in num:
            # Subtract 1 to get the correct index since Python lists are zero-based
            index = n - 1
            uuid = get_unused_uuid(index)
            if uuid:
                executor.submit(process_chrome_profile, n, uuid)

TestScript()
print("Error profiles:", error_profiles)
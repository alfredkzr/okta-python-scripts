from dotenv import load_dotenv
import os
import requests
import json
import time
import datetime
import pandas as pd
from urllib.parse import parse_qs, urlparse

load_dotenv()

today = datetime.datetime.today().date()
formatted_date = today.strftime("%d-%m-%Y")
print(f"📅 Today is: {formatted_date}")

#create a .env file for api_key 
token = os.getenv("API_KEY_PROD")
oktaOrg = 'enter your okta org here'
    
def get_devices():
    device_count = 0
    url = f"https://{oktaOrg}.okta.com/api/v1/devices?expand=user"
    api_request_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "SSWS {}".format(token)
    }
    #intialise list of okta users
    okta_devices = []
    done = False
    after_token = None
    
    #Loop through the request
    while not done:
        #Set to 50 users max per request
        device_count+=50
        print(f"Retrieving device information from Okta... {device_count} devices")
        params = {
            'limit': 50,
        }

        #Use the after if exists
        if after_token:
            params['after'] = after_token

        #API request
        device_response = requests.get(
            url=url,
            params=params,
            headers=api_request_headers
        )

        #exception error
        if device_response.status_code != 200:
            raise Exception("Got HTTP {} listing users",
                            device_response.status_code)

        response = device_response.json()

        okta_devices.extend([x for x in response])

        #paginate with next url
        if 'next' in device_response.links:
            next_url = device_response.links['next']['url']
            after_token = parse_qs(urlparse(next_url).query)['after'][0]
        else:
            done = True
            
    return okta_devices

print(f"Retrieving devices information from Okta...")
devices = get_devices()
print(f"Found {len(devices)} devices")
#print(json.dumps(devices, indent=2))

'''Save as JSON file'''
with open(f'okta_devices_{formatted_date}.json', 'w') as outfile:
    json.dump(devices, outfile)

'''Save as CSV file but embedded section is not flattened'''
json_normalized = pd.json_normalize(devices)
json_normalized.to_csv(f"okta_devices_{formatted_date}.csv")
print(f"okta_devices_{formatted_date}.csv exported successfully!")
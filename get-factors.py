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

#use a .env file to store your api key
token = os.getenv("API_KEY_PROD")
oktaOrg = 'enter your okta org here'

#You may need to change the path of this users.txt file. Enter usernames line by line in this file.
with open("Okta/users.txt") as f:
    userNames = f.read().strip().split("\n")

user_factors = []

def get_user(userName):
    url = f"https://{oktaOrg}.okta.com/api/v1/users/?search=profile.login%20eq%20%22{userName}%22"

    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': "SSWS {}".format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    userInfo = json.loads(response.text)
    return userInfo
    

def get_factors(userId, userName):
    print(f"Retrieving factors info from {userName}...")
    url = f"https://{oktaOrg}.okta.com/api/v1/users/{userId}/factors"
    api_request_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "SSWS {}".format(token)
    }
    
    factor_response = requests.get(
    url=url,
    headers=api_request_headers
    )
    
    response = factor_response.json()

    #manually add a key 'userName' to every row so we can identity user easily
    for factor in response:
        factor['userName'] = userName
    
    return response

print(f"Retrieving users factors from Okta...")
    
for userName in userNames:
    userData = get_user(userName)
    userId = userData[0]['id']
    factor = get_factors(userId,userName)
    user_factors.extend([x for x in factor])

'''Save as CSV file but embedded section is not flattened'''
json_normalized = pd.json_normalize(user_factors)
json_normalized.to_csv(f"okta_users_factors_{formatted_date}.csv")
print(f"okta_users_factors_{formatted_date}.csv exported successfully!")
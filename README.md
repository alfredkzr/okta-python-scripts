# okta-python-scripts
This repo is to document the scripts that I've created that aren't typically provided in the Okta Python SDK.

# How to authenticate
Please generate a basic API key in Okta to use against the API call.

https://developer.okta.com/docs/guides/create-an-api-token/main/

## get-devices.py
This script can retrieve all devices including user information embedded and export it into both JSON and normalised CSV file for easy reference.

## get-factors.py
This script uses a list of users you indicate in a .txt file and retrieve all factors belonging to the user. This is especially useful when you need granular information such authenticatorName which can contain the AAGUID of security keys (e.g. Yubikey 5Ci).
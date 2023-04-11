import requests
import json

base_url = 'https://us.api.insight.rapid7.com/ias/v1'
api_key = 'd64311f2-f524-4ce0-a6ac-b0ba8391065e'
headers = {'X-Api-Key': api_key, 'Content-Type': 'application/json'}

# Fetch the list of applications
applications_url = f'{base_url}/apps'
response = requests.get(applications_url, headers=headers)

try:
    applications = response.json()
    print("Applications:", applications)  # Print the applications data for debugging purposes
except json.JSONDecodeError:
    print("Error: Unable to parse JSON data")
    applications = []

# Choose the desired application and get its ID
id = None
for app in applications:
    if isinstance(app, dict) and 'name' in app and 'id' in app and app['name'] == 'staging.beyondfinance.com':
        id = app['id']
        break

# Fetch the list of vulnerabilities for the chosen application
if id:
    vulnerabilities_url = f'{base_url}/apps/{id}/vulnerabilities'
    response = requests.get(vulnerabilities_url, headers=headers)
    vulnerabilities = response.json()

    # Process and store the vulnerabilities as needed
    # (for example, save them to a JSON file)
    with open('vulnerabilities.json', 'w') as outfile:
        json.dump(vulnerabilities, outfile)

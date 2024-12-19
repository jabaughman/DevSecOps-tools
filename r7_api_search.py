import requests
import json
from datetime import datetime

base_url = 'https://us.api.insight.rapid7.com/ias/v1'
api_key = ''
headers = {'X-Api-Key': api_key, 'Content-Type': 'application/json'}

# Set your desired query
appQuery = "vulnerability.app.id = 'd3f93c30-e97d-4dc4-8898-88eac1c833db' && vulnerability.severity = 'Low' || vulnerability.severity = 'Medium' || vulnerability.severity = 'High' && vulnerability.status = 'UNREVIEWED'"
query = 'your_query_string'  # Replace with your actual query string

# Prepare the payload
payload = {
    "query": appQuery,
    "type": "VULNERABILITY"
}

# Perform the search
search_url = f'{base_url}/search'
response = requests.post(search_url, headers=headers, data=json.dumps(payload))

try:
    search_response = response.json()
    ##print("Search Response:", search_response)
    with open('ALL_DATA.json', 'w') as outfile:
        json.dump(search_response, outfile)
except json.JSONDecodeError:
    print("Error: Unable to parse JSON data")
    search_response = {}

# Process and store the vulnerabilities as needed
if 'data' in search_response:
    unreviewed_vulnerabilities = []
    most_recent_date = None

    for vulnerability in search_response.get("data", []):
        last_discovered = vulnerability.get("last_discovered")
        if last_discovered:
            last_discovered_date = datetime.strptime(last_discovered, '%Y-%m-%dT%H:%M:%S.%f')
            if not most_recent_date or last_discovered_date > most_recent_date:
                most_recent_date = last_discovered_date
                print("Updated most recent date:", most_recent_date)
    
    if most_recent_date:
        for vulnerability in search_response.get("data", []):
            last_discovered = vulnerability.get("last_discovered")
            if last_discovered:
                last_discovered_date = datetime.strptime(last_discovered, '%Y-%m-%dT%H:%M:%S.%f')
                if last_discovered_date == most_recent_date and vulnerability.get("status") == "UNREVIEWED":
                    unreviewed_vulnerabilities.append(vulnerability)
                    print("Unreviewed Vulnerabilities", unreviewed_vulnerabilities)
                else:
                    #print("Skipped vulnerabilities:", vulnerability)
                    with open('skipped_vulnerabilities.json', 'w') as outfile:
                        json.dump(vulnerability, outfile)

    # (for example, save them to a JSON file)
    with open('vulnerabilities.json', 'w') as outfile:
        json.dump(unreviewed_vulnerabilities, outfile)
else:
    print("Error: No vulnerabilities found")

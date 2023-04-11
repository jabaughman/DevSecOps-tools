import requests
import json
from datetime import datetime
from dateutil.parser import isoparse

base_url = 'https://us.api.insight.rapid7.com/ias/v1'
api_key = 'd64311f2-f524-4ce0-a6ac-b0ba8391065e'
headers = {'X-Api-Key': api_key, 'Content-Type': 'application/json'}

reports_url = f'{base_url}/reports'
response = requests.get(reports_url, headers=headers)

try:
    reports = response.json()
    print("Reports:", reports)  # Print the applications data for debugging purposes
except json.JSONDecodeError:
    print("Error: Unable to parse JSON data")
    reports = []

# Find the most recent report
most_recent_date = None
most_recent_report_id = None

for report in reports['data']:
    generated_date = isoparse(report['generated_date'])
    if most_recent_date is None or generated_date > most_recent_date:
        most_recent_date = generated_date
        most_recent_report_id = report['id']

if most_recent_report_id:
    # Download the most recent report in CSV Format
    report_url = f'{base_url}/reports/{most_recent_report_id}'
    headers['Accept'] = 'text/csv,application/json'
    response = requests.get(report_url, headers=headers)

    if response.status_code == 200:
        # Save the report as a CSV File
        with open('appsec_findings.csv', 'wb') as f:
            f.write(response.content)
            print('Report save as appsec_findings.csv')
    else:
        print(f"Error downliading report: {response.status_code} {response.text}")
else:
    print("No reports found")

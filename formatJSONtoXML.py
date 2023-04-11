import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    raw_str = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(raw_str)
    return reparsed.toprettyxml(indent="  ")

input_file = 'appsec_findings.csv'
output_file = 'appsec_findings_burp.xml'

# Read CSV file and create XML structure
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    issues = ET.Element('issues')
    
    for row in reader:
        issue = ET.SubElement(issues, 'issue')

        ET.SubElement(issue, 'type').text = row['attackType']
        ET.SubElement(issue, 'serialNumber').text = row['uuid']
        ET.SubElement(issue, 'name').text = row['moduleName']
        ET.SubElement(issue, 'severity').text = row['severity']
        ET.SubElement(issue, 'app_name').text = row['app_name']
        ET.SubElement(issue, 'app_description').text = row['app_description']
        ET.SubElement(issue, 'app_uuid').text = row['app_uuid']
        ET.SubElement(issue, 'rootCause_url').text = row['rootCause_url']
        ET.SubElement(issue, 'rootCause_parameter').text = row['rootCause_parameter']
        ET.SubElement(issue, 'rootCause_method').text = row['rootCause_method']
        ET.SubElement(issue, 'status').text = row['status']
        ET.SubElement(issue, 'scanType').text = row['scanType']

# Save the XML file
with open(output_file, 'w', encoding='utf-8') as xmlfile:
    xmlfile.write(prettify(issues))
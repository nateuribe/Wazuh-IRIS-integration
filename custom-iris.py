#!/usr/bin/env python3
# custom-iris.py
# Custom Wazuh integration script to send alerts to DFIR-IRIS

import sys
import json
import requests
from requests.auth import HTTPBasicAuth

# Read parameters when integration is run
alert_file = sys.argv[1]
api_key = sys.argv[2]
hook_url = sys.argv[3]

# Read the alert file
with open(alert_file) as f:
    alert_json = json.load(f)

# Extract field information
alert_id = alert_json["id"]
alert_timestamp = alert_json["timestamp"]
alert_level = alert_json["rule"]["level"]
alert_description = alert_json["rule"]["description"]
agent_name = alert_json["agent"]["name"]
rule_id = alert_json["rule"]["id"]

# Convert Wazuh rule levels -> IRIS severity
if(alert_level < 5):
    severity = 2
elif(alert_level >= 5 and alert_level < 7):
    severity = 3
elif(alert_level >= 7 and alert_level < 10):
    severity = 4
elif(alert_level >= 10 and alert_level < 13):
    severity = 5
elif(alert_level >= 13):
    severity = 6
else:
    severity = 1

# Generate request
# Reference: https://docs.dfir-iris.org/_static/iris_api_reference_v2.0.1.html#tag/Alerts/operation/post-case-add-alert
payload = json.dumps({
    "alert_title": "Wazuh Alert",
    "alert_description": alert_description,
    "alert_source": "Wazuh Server",
    "alert_source_ref": alert_id,
    "alert_source_link": "**WAZUH_URL**,
    "alert_severity_id": severity, 
    "alert_status_id": 2, # 'New' status
    "alert_source_event_time": alert_timestamp,
    "alert_note": "",
    "alert_tags": "wazuh," + agent_name,
    "alert_customer_id": 1, # '1' for default 'IrisInitialClient'
    "alert_source_content": alert_json # raw log
})

# Send request to IRIS
response = requests.post(hook_url, data=payload, headers={"Authorization": "Bearer " + api_key, "content-type": "application/json"})

sys.exit(0)

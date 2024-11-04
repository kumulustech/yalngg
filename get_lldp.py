import os
import csv
import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
SW_ADMIN = os.getenv('SW_ADMIN')
SW_PASS = os.getenv('SW_PASS')

# Load the list of devices from the CSV file
def load_devices(csv_file):
    devices = []
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            devices.append(row)
    return devices

# Fetch LLDP data from a device
def fetch_lldp_data(switch_ip):
    url = f"https://{switch_ip}/restconf/data/openconfig-lldp:lldp/interfaces/interface"
    response = requests.get(url, auth=HTTPBasicAuth(SW_ADMIN, SW_PASS), verify=False)
    response.raise_for_status()
    return response.json()

# Gather LLDP data for all devices
def gather_lldp_data(devices):
    all_lldp_data = {}
    
    for device in devices:
        hostname = device['hostname']
        switch_ip = device['switchip']
        
        try:
            lldp_data = fetch_lldp_data(switch_ip)
            all_lldp_data[hostname] = lldp_data
        except Exception as e:
            print(f"Error fetching data for {hostname}: {e}")
    
    return all_lldp_data

def main():
    csv_file = 'switches.csv'
    devices = load_devices(csv_file)
    all_lldp_data = gather_lldp_data(devices)
    
    # Save the data to a JSON file
    with open('lldp_data.json', 'w') as outfile:
        json.dump(all_lldp_data, outfile, indent=4)

if __name__ == "__main__":
    main()

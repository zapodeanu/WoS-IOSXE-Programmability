

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import requests
import json
import os
os.chdir("/bootflash/WoS-Demo")


from config import DEV_USER, DEV_PASSW, DEV_IP

from requests.auth import HTTPBasicAuth  # for Basic Auth

DEV_AUTH = HTTPBasicAuth(DEV_USER, DEV_PASSW)

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


def get_restconf_hostname(host_ip):

    # retrieve the hostname of the device with the {host_ip} using restconf

    url = 'https://' + host_ip + '/restconf/data/Cisco-IOS-XE-native:native/hostname'
    header = {'Content-type': 'application/yang-data+json', 'accept': 'application/yang-data+json'}
    response = requests.get(url, headers=header, verify=False, auth=DEV_AUTH)
    hostname_json = response.json()
    hostname = hostname_json['Cisco-IOS-XE-native:hostname']
    return hostname




# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import dnac_apis
import service_now_apis
import restconf

import time
import requests
import os

from cli import cli

from config import SNOW_ADMIN, SNOW_DEV, SNOW_PASS, SNOW_URL
from config import DNAC_URL, DNAC_PASS, DNAC_USER
from config import DEV_IP, DEV_USER, DEV_PASSW

from requests.auth import HTTPBasicAuth  # for Basic Auth

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


os.chdir("/bootflash/WoS-Demo")

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


# collect the syslog entry that triggered the event
syslog_input = cli("show logging | in %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/0/13, changed state to down")
syslog_lines = syslog_input.split("\n")
lines_no = len(syslog_lines) - 2
syslog_info = syslog_lines[lines_no]


# retrieve the device hostname using RESTCONF
device_name = restconf.get_restconf_hostname(DEV_IP)


# retrieve the serial number using Python cli
device_info = cli("sh ver | in System Serial Number")
device_info_list = device_info.split(' ')
device_sn = device_info_list[-1]


# retrieve the device location using DNA C REST APIs
dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
location = dnac_apis.get_device_location(device_name, dnac_token)


# define the incident description and comment
short_description = "Switch Critical Interface Down - IOS XE Automation"
comment = "The device with the name: " + device_name + "\n has detected an Critical Interface Down"
comment += "\n\nThe device serial number: " + device_sn
comment += "\nThe device location is: " + location
comment += "\n\nSyslog: " + syslog_info


# create a new ServiceNow incident using ServiceNow REST APIs
incident = service_now_apis.create_incident(short_description, comment, SNOW_DEV, 1)


# write the new incident name to file in /bootflash/WoS-Demo
incident_file = open("/bootflash/WoS-Demo/critical_interface_ticket.txt", "w")
incident_file.write(incident)
incident_file.close()


print("End Application Run - Critical Interface Down")

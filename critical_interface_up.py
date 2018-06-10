

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
syslog_input = cli("show logging | in %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet1/0/13, changed state to up")
syslog_lines = syslog_input.split("\n")
lines_no = len(syslog_lines) - 2
syslog_info = syslog_lines[lines_no]


# retrieve the device hostname using RESTCONF
device_name = restconf.get_restconf_hostname(DEV_IP)


# define the incident description and comment
update_comment = "The device with the name: " + device_name + "\n has recovered from a Critical Interface Down condition"
update_comment += "\n\nSyslog: " + syslog_info


# find the ServiceNow incident
file = open("critical_interface_ticket.txt", "r")
incident = file.read()
file.close()


# update the ServiceNow incident using ServiceNow REST APIs
service_now_apis.update_incident(incident, update_comment, SNOW_DEV)


# close ServiceNow incident using ServiceNow REST APIs
time.sleep(1)
service_now_apis.close_incident(incident, SNOW_DEV)


# delete the incident name from the file in /bootflash/WoS-Demo
incident_file = open("/bootflash/WoS-Demo/critical_interface_ticket.txt", "w")
incident_file.write("INCIDENT")
incident_file.close()


print("End Application Run - Critical Interface Up")

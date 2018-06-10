

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


# read the syslog entry that triggered the event using Python cli
syslog_input = cli("show logging | in %PLATFORM_FEP-6-FRU_PS_OIR: Switch 1: FRU power supply A powered on")
syslog_lines = syslog_input.split("\n")
lines_no = len(syslog_lines)-2
syslog_info = syslog_lines[lines_no]


# retrieve the device hostname using RESTCONF
device_name = restconf.get_restconf_hostname(DEV_IP)


# define the incident description and comment
update_comment = "The device with the: " + device_name + "\n has recovered from the Redundant Power Supply failure"
update_comment += "\n\nSyslog: " + syslog_info + "\n\nSwitch Beacon LED turned OFF"


# find the ServiceNow incident cached on the switch flash memory
file = open("power_ticket.txt", "r")
incident = file.read()
file.close()


# update the ServiceNow incident using ServiceNow REST APIs
service_now_apis.update_incident(incident, update_comment, SNOW_DEV)


# close ServiceNow incident
time.sleep(1)
service_now_apis.close_incident(incident, SNOW_DEV)


# delete the incident name from the file in /bootflash/WoS-Demo
incident_file = open("/bootflash/WoS-Demo/power_ticket.txt", "w")
incident_file.write("INCIDENT")
incident_file.close()


time.sleep(1)


# turn off the blue beacon LED on the device
cli("configure terminal\nhw-module beacon off switch 1")


print("End Application Run - Power Supply Recovery")


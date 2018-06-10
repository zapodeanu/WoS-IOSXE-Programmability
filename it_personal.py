

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import service_now_apis
import spark_apis
import time
import requests
import os
import utils


from config import SNOW_ADMIN, SNOW_DEV, SNOW_PASS, SNOW_URL
from config import SPARK_ROOM

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

ITPA_USER = "Jim"
ITPA_EMAIL = "gabriel.zapodeanu@gmail.com"


def main():
    """
    This IT Personal Assistant App will:
    - locate the user using MDM or CMX
    - when user arrives to the office it will create a Spark Room and welcome the user to the office
    - it will check for any open Service Now incidents from the caller IOS XE
    - post the summary of the incidents in Spark
    """

    # start application when user in the office
    raw_input('Enter any key when user in the office: ')

    # retrieve the tickets info for the last 50 tickets
    incidents_info = service_now_apis.get_last_incidents_info(50)

    # select the tickets that are created by SNOW_DEV
    incident_list = []
    for incident in incidents_info:
        if incident["sys_created_by"] == SNOW_DEV:
            incident_list.append(incident["number"])
    print("All Open IOS XE Automation Incidents: ")
    utils.pprint(incident_list)

    # select the tickets that are created by SNOW_DEV and still open and urgent
    incident_urgent = []
    for incident in incidents_info:
        if incident["sys_created_by"] == SNOW_DEV:
            if incident["state"] == "1":
                incident_urgent.append(incident["number"])
    print("Open IOS XE Automation Critical Incidents: ")
    utils.pprint(incident_urgent)


    # create Spark Room and invite user
    room_id = spark_apis.create_room(SPARK_ROOM)
    spark_apis.add_room_membership(room_id, ITPA_EMAIL)
    spark_apis.post_room_markdown_message(room_id, (ITPA_USER + " ---  Welcome to the office"))

    if incident_urgent == []:
        spark_apis.post_room_message(room_id, "No open critical incidents since yesterday afternoon")
    else:
        spark_apis.post_room_message(room_id, "These are the critical open incidents: \n")
        for incident in incident_urgent:
            incident_detail = service_now_apis.get_incident_detail(incident)
            spark_apis.post_room_url_message(room_id, (incident_detail["number"]), (
                        "https://dev48476.service-now.com/nav_to.do?uri=incident.do?sys_id=" + incident_detail["sys_id"]))
            spark_apis.post_room_message(room_id, "Description: " + incident_detail["short_description"])

    raw_input('\nReady to reset demo?  ')
    # reset state for next demo
    # delete Spark room
    spark_apis.delete_room(room_id)
    print('\nSpark Room with the name: ' + SPARK_ROOM + ' deleted')

    # delete Service Now incidents
    for incident in incident_list:
        service_now_apis.delete_incident(incident)

    print('\nDeleted all IOX Automation created incidents')
    print('\n\nEnd of Application Run IT Personal Assistant')

if __name__ == '__main__':
    main()
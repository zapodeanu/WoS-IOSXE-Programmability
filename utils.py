

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


# this module includes common utilized utility functions

import json
import requests


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


def pprint(json_data):

    # Pretty print JSON formatted data

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_input_ip():

    # This function will ask the user to input the IP address. The format of the IP address is not validated

    ip_address = input('Input the IP address to be validated, (or q to exit) ?  ')
    return ip_address


def get_input_mac():

    # This function will ask the user to input the IP address. The format of the IP address is not validated

    mac_address = input('Input the MAC address to be validated, (or q to exit) ?  ')
    return mac_address


def get_input_timeout(message, wait_time):

    # This function will ask the user to input the value requested in the {message}, in the time specified {time}

    print(message + ' in ' + str(wait_time) + ' seconds')
    i, o, e = select.select([sys.stdin], [], [], wait_time)
    if i:
        input_value = sys.stdin.readline().strip()
        print('User input: ', input_value)
    else:
        input_value = None
        print('No user input in ', wait_time, ' seconds')
    return input_value

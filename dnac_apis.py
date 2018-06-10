

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


import requests
import json

from requests.auth import HTTPBasicAuth  # for Basic Auth

from config import DNAC_URL, DNAC_PASS, DNAC_USER

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data: data to pretty print
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access DNA C
    Call to DNA C - /api/system/v1/auth/login
    :param dnac_auth - DNA C Basic Auth string
    :return: DNA C JWT token
    """

    url = DNAC_URL + '/api/system/v1/auth/login'
    header = {'content-type': 'application/json'}
    response = requests.get(url, auth=dnac_auth, headers=header, verify=False)
    response_header = response.headers
    dnac_jwt_token = response_header['Set-Cookie']
    return dnac_jwt_token


def get_all_device_info(dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/api/v1/network-device'
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    all_device_response = requests.get(url, headers=header, verify=False)
    all_device_info = all_device_response.json()
    return all_device_info['response']


def get_device_info(device_id, dnac_jwt_token):
    """
    This function will retrieve all the information for the device with the DNA C device id
    :param device_id: DNA C device_id
    :param dnac_jwt_token: DNA C token
    :return: device info
    """
    url = DNAC_URL + '/api/v1/network-device?id=' + device_id
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    return device_info['response']


def get_client_info(client_ip, dnac_jwt_token):
    """
    This function will retrieve all the information from the client with the IP address
    :param client_ip: client IPv4 address
    :param dnac_jwt_token: DNA C token
    :return: client info, or {None} if client does not found
    """
    url = DNAC_URL + '/api/v1/host?hostIp=' + client_ip
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    client_json = response.json()
    try:
        client_info = client_json['response'][0]
        return client_info
    except:
        return None


def locate_client_ip(client_ip, dnac_jwt_token):
    """
    Locate a wired client device in the infrastructure by using the client IP address
    Call to DNA C - api/v1/host?hostIp={client_ip}
    :param client_ip: Client IP Address
    :param dnac_jwt_token: DNA C token
    :return: hostname, interface_name, vlan_id, or None, if the client does not exist
    """

    client_info = get_client_info(client_ip, dnac_jwt_token)
    if client_info is not None:
        hostname = client_info['connectedNetworkDeviceName']
        interface_name = client_info['connectedInterfaceName']
        vlan_id = client_info['vlanId']
        return hostname, interface_name, vlan_id
    else:
        return None


def get_device_status(device_name, dnac_jwt_token):
    """
    This function will return the reachability status for the network device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: status - {UNKNOWN} to locate a device in the database,
                      {SUCCESS} device reachable
                      {FAILURE} device not reachable
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    if device_id is None:
        return 'UNKNOWN'
    else:
        device_info = get_device_info(device_id, dnac_jwt_token)
        if device_info['reachabilityStatus'] == 'Reachable':
            return 'SUCCESS'
        else:
            return 'FAILURE'


def get_device_management_ip(device_name, dnac_jwt_token):
    """
    This function will find out the management IP address for the device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: the management ip address
    """
    device_ip = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_ip = device['managementIpAddress']
    return device_ip


def get_device_id_sn(device_sn, dnac_jwt_token):
    """
    The function will return the DNA C device id for the device with serial number {device_sn}
    :param device_sn: network device SN
    :param dnac_jwt_token: DNA C token
    :return: DNA C device id
    """
    url = DNAC_URL + '/api/v1/network-device/serial-number/' + device_sn
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    device_id = device_info['response']['id']
    return device_id


def get_device_id_name(device_name, dnac_jwt_token):
    """
    This function will find the DNA C device id for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return:
    """
    device_id = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_id = device['id']
    return device_id


def get_device_location(device_name, dnac_jwt_token):
    """
    This function will find the location for the device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: the location
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/group/member/' + device_id + '?groupType=SITE'
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = (device_response.json())['response']
    device_location = device_info[0]['groupNameHierarchy']
    return device_location


def check_ipv4_network_interface(ip_address, dnac_jwt_token):
    """
    This function will check if the provided IPv4 address is configured on any network interfaces
    :param ip_address: IPv4 address
    :param dnac_jwt_token: DNA C token
    :return: None, or device_hostname and interface_name
    """
    url = DNAC_URL + '/api/v1/interface/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    try:
        response_info = response_json['response'][0]
        interface_name = response_info['portName']
        device_id = response_info['deviceId']
        device_info = get_device_info(device_id, dnac_jwt_token)
        device_hostname = device_info['hostname']
        return device_hostname, interface_name
    except:
        device_info = get_device_info_ip(ip_address, dnac_jwt_token)  # required for AP's
        device_hostname = device_info['hostname']
        return (device_hostname,)


def get_device_info_ip(ip_address, dnac_jwt_token):
    """
    This function will retrieve the device information for the device with the management IPv4 address {ip_address}
    :param ip_address: device management ip address
    :param dnac_jwt_token: DNA C token
    :return: device information, or None
    """
    url = DNAC_URL + '/api/v1/network-device/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    device_info = response_json['response']
    if 'errorCode' == 'Not found':
        return None
    else:
        return device_info


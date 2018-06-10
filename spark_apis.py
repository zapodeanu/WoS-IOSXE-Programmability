

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems


# this module includes common utilized functions to create applications using Spark APIs


import requests
import json

from config import SPARK_AUTH, SPARK_URL

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings


def create_room(room_name):

    # create spark room

    payload = {'title': room_name}
    url = SPARK_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    room_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    room_json = room_response.json()
    room_id = room_json['id']
    print('Created room with the name ' + room_name)
    return room_id


def add_room_membership(room_id, email_invite):

    # invite membership to the room id

    payload = {'roomId': room_id, 'personEmail': email_invite, 'isModerator': 'true'}
    url = SPARK_URL + '/memberships'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    membership_response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    membership_json = membership_response.json()
    try:
        membership = membership_json['personEmail']
    except:
        membership = None
    return membership


def delete_room(room_id):

    # delete room with the room id

    url = SPARK_URL + '/rooms/' + room_id
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    requests.delete(url, headers=header, verify=False)


def post_room_message(room_id, message):

    # post message to the Spark room with the room id

    payload = {'roomId': room_id, 'text': message}
    url = SPARK_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def post_room_markdown_message(room_id, message):

    # post message to the Spark room with the room id

    payload = {'roomId': room_id, 'markdown': ('**' + message + '**')}
    url = SPARK_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def post_room_url_message(room_id, message, url):

    # post message to the Spark room with the room id

    payload = {'roomId': room_id, 'markdown': ('[' + message + '](' + url + ')')}
    url = SPARK_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def last_user_message(room_id):

    # retrieve the last message from the room with the room id

    url = SPARK_URL + '/messages?roomId=' + room_id
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    response = requests.get(url, headers=header, verify=False)
    list_messages_json = response.json()
    list_messages = list_messages_json['items']
    last_message = list_messages[0]['text']
    return last_message


def get_room_id(room_name):

    # This function will find the Spark room id based on the {room_name}

    payload = {'title': room_name}
    room_number = None
    url = SPARK_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': SPARK_AUTH}
    room_response = requests.get(url, data=json.dumps(payload), headers=header, verify=False)
    room_list_json = room_response.json()
    room_list = room_list_json['items']
    for rooms in room_list:
        if rooms['title'] == room_name:
            room_number = rooms['id']
    return room_number


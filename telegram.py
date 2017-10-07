import urllib
import requests
import os

token = ""
owner_id = 0
base = "https://api.telegram.org/"
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def get_updates():
    parameter = "/getUpdates"
    response = requests.get(base + token + parameter).json()["result"]
    last_message_file = open(os.path.join(THIS_FOLDER, "last_message.inf"), "r")
    last_message = last_message_file.read()
    last_message_file.close()
    last_message = int(last_message)

    if len(response) == 0:
        return []

    message_list = []
    for update in response:
        if update.get("message") is not None:
            msg_type = "message"
        else:
            msg_type = "edited_message"
        if update[msg_type]["from"]["id"] == owner_id and update[msg_type]["message_id"] > last_message:
            message_list.append(update[msg_type])

    if len(message_list) == 0:
        return []

    last_message_file = open(os.path.join(THIS_FOLDER, "last_message.inf"), "w")
    last_message_file.write(str(message_list[len(message_list) - 1].get("message_id")))
    last_message_file.close()

    return message_list


def send(message):
    print("Sending answer")
    parameter = "/sendMessage?chat_id=" + str(owner_id) + "&text="
    message = urllib.request.quote(message)
    urllib.request.urlopen(base + token + parameter + message)

    print("Sent!")

    return 0

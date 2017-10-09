import telegram
import json
import os
import time

FILES_FOLDER = os.path.dirname(os.path.abspath(__file__))
owner_id = 287322046
limit = 40


def main():
    while True:
        time.sleep(1)
        try:
            play()
        except:
            telegram.send("What have you done? :(\nNow bot is down ((9(")
            continue


def play():
    telegram.token = "bot198334737:AAH3Z-0Gu1TqnVj6H8Zs3f4OS8u71JeX5Jc"
    telegram.owner_id = owner_id
    messages = telegram.get_updates()

    if messages != []:
        print(str(len(messages)) + " new messages was found")
        message = messages[len(messages) - 1]["text"]

        is_running = open(os.path.join(FILES_FOLDER, "is_running.txt"), "r")
        is_dangerous = is_running.read()
        is_running.close()

        if is_dangerous == "1":
            telegram.send("Daniel is gonna post, don't disturb him.\nJust let him done his job (because he has one).")
            return

        if message[:9] == "/get_logs":
            answer = get_post_owners(message[10:])
        elif message[:8] == "/get_log":
            answer = get_post_publisher(message[9:])
        elif message[:12] == "/get_victims":
            answer = get_victims(message[13:])
        elif message[:11] == "/add_victim":
            add_victim(message[12:])
            answer = get_victims()
        elif message[:11] == "/del_victim":
            returned = del_victim(message[12:])
            if returned == 0:
                answer = get_victims()
            else:
                answer = str(returned)
        else:
            answer = "What a fuck are you talking about?"
        telegram.send(answer)
    print("done!")


def get_post_publisher(post_id):
    post_id = post_id.strip()

    post_owner_file = open(os.path.join(FILES_FOLDER, "post_owner.txt"), "r")
    post_owner = post_owner_file.read()
    post_owner_file.close()

    right_side = post_owner[index_of(post_owner, post_id + " from -"):]
    post_owner_string = right_side[:index_of(right_side, "\n")]
    post_owner_link = "vk.com/public" + post_owner_string[index_of(post_owner_string, "-") + 1:]

    return post_owner_link


def get_post_owners(count):
    count = count.strip()

    post_owner_file = open(os.path.join(FILES_FOLDER, "post_owner.txt"), "r")
    post_owner = post_owner_file.readlines()
    post_owner_file.close()

    if count == "":
        count = 9
    else:
        try:
            count = int(count)
            if count > len(post_owner) - 1:
                count = len(post_owner) - 1
        except:
            return "It seems like parameter is not number, dude."

    post_owner_string = ""
    if count > limit:
        count = limit
        post_owner_string += "Have you got any mental disorders?\nYou can't get more than " + str(limit) + " records, so here you are:\n"

    i = 0
    while i < count:
        post_owner_string += str(post_owner[i])
        i += 1

    return post_owner_string


def get_victims(with_last=""):
    with_last = with_last.strip()
    victims = json.load(open(os.path.join(FILES_FOLDER, "victims.txt"), "r"))
    victims_str = FILES_FOLDER
    i = 1
    for victim in victims:
        if with_last == "+":
            victims_str += str(i) + ". vk.com/" + victim["id"]
            # victims_str += "\nlast: " + str(victim["last"])
        else:
            victims_str += str(i) + ". " + victim["id"]
        victims_str += "\n"
        i += 1

    return victims_str


def add_victim(pub_id):
    pub_id = pub_id.strip()
    victims = json.load(open(os.path.join(FILES_FOLDER, "victims.txt"), "r"))
    new_victim = {"id": pub_id, "delta": 0, "last": 0}
    victims.append(new_victim)
    json.dump(victims, open(os.path.join(FILES_FOLDER, "victims.txt"), "w"))
    return 0


def del_victim(pub_num):
    pub_num = pub_num.strip()
    victims = json.load(open(os.path.join(FILES_FOLDER, "victims.txt"), "r"))

    try:
        pub_num = int(pub_num) - 1
        del victims[pub_num]
    except Exception as ex_msg:
        return ex_msg

    json.dump(victims, open(os.path.join(FILES_FOLDER, "victims.txt"), "w"))
    return 0


def index_of(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1


if __name__ == "telegram_main":
    main()

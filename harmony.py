'''
harmony.py
This script deletes every message and DM you have ever sent on discord
Requirements:
pip3 install requests
Usage:
python3 ./harmony.py
'''
import requests
import time

def auth_headers(token):
    return {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }

def get_auth_token(email, password):
    url = 'https://discordapp.com/api/v6/auth/login' 
    headers = {"Content-Type": "application/json"}
    data = '{"email":"' + email +'","password":"' + password + '","undelete":"false","captcha_key":"null"}'
    r = requests.post(url, headers = headers, data = data)
    request_json = r.json()
    return request_json['token']


def get_user_id(token):
    url = 'https://discordapp.com/api/users/@me'
    headers = auth_headers(token)
    r = requests.get(url, headers = headers)
    request_json = r.json()
    return request_json['id']


def get_guild_channels(token):
    url = 'https://discordapp.com/api/v6/users/@me/guilds'
    headers = auth_headers(token)
    r = requests.get(url, headers = headers)
    request_json = r.json()
    guildList = []
    for guild in request_json:
        guildList.append(guild['id'])
    return guildList

def get_dm_channels(token):
    url = 'https://discordapp.com/api/users/@me/channels'
    headers = auth_headers(token)
    r = requests.get(url, headers = headers)
    request_json = r.json()
    channelList = []
    for channel in request_json:
        channelList.append(channel["id"])
    return channelList

def delete_message(channel, msg_id, token):
    url = 'https://discordapp.com/api/channels/' + channel + '/messages/' + msg_id
    headers = auth_headers(token)
    r = requests.delete(url, headers = headers)
    if r.status_code == 204:
        print("Deleted ", channel, " ", msg_id)


if __name__ == "__main__":
    print("Enter your discord username (email address): ")
    email = input()

    print("Enter your password: ")
    password = input()

    token = get_auth_token(email, password)
    print("Token: " ,token)
    time.sleep(1)

    my_id = get_user_id(token)
    print("My ID: ", my_id)
    time.sleep(1)

    guildList = get_guild_channels(token)
    time.sleep(1)

    channelList = get_dm_channels(token)
    time.sleep(1)

    toBeDeleted =[]

    print("Searching for messages in all guild channels")

    for guild in guildList:
        offset = 0
        totalMessages = 99999999
        while offset <= totalMessages:
            url = 'https://discordapp.com/api/guilds/' + guild + '/messages/search?author_id=' + my_id + '&offset=' + str(offset)
            r = requests.get(url, headers = headers)
            objB = r.json()
            totalMessages = objB['total_results']
            for stuff in objB['messages']:
                for message in stuff:
                    if 'hit' in message:
                        if message['author']['id'] == my_id:
                            print(message['channel_id'],message['id'])
                            toBeDeleted.append([message['channel_id'],message['id']])
            offset += 25
            time.sleep(.5)

    print("Searching for messages in all DM channels")
    for channel in channelList:
        messageList = []
        url = 'https://discordapp.com/api/channels/' +channel+ '/messages'
        r = requests.get(url, headers = headers)
        objB = r.json()
        for message in objB:
            messageList.append(message['id'])
            if message['author']['id'] == my_id:
                toBeDeleted.append([channel,message['id']])
                print(channel,message['id'])

        tempvalue = ''
        scrape = True
        while scrape:
            messageList.sort()
            if len(messageList):
                tempvalue = messageList[0]
                url = 'https://discordapp.com/api/channels/' +channel+ '/messages?limit=100&before='+ messageList[0]
                r = requests.get(url, headers = headers)
                objC = r.json()
                for message in objC:
                    messageList.append(message['id'])
                    if message['author']['id'] == my_id:
                        print(channel,message['id'])
                        toBeDeleted.append([channel,message['id']])
            messageList.sort()
            if not len(messageList) or tempvalue == messageList[0]:
                scrape = False
            time.sleep(.5)

    print("You are about to delete ", len(toBeDeleted), "messages.")
    if input("Proceed? y/n") == 'y':
        for [channel, msg_id] in toBeDeleted:
            delete_message(channel, msg_id, token)
            time.sleep(.25)

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


print("Enter your discord username (email address): ")
email = input()

print("Enter your password: ")
password = input()

#Getting auth token
url = 'https://discordapp.com/api/v6/auth/login' 
headers = {"Content-Type": "application/json"}
data = '{"email":"' + email +'","password":"' + password + '","undelete":"false","captcha_key":"null"}'
r = requests.post(url, headers = headers, data = data)
objToken = r.json()
token = objToken['token']
print("Token: " ,token)
time.sleep(1)

#Getting UserID
url = 'https://discordapp.com/api/users/@me'
headers = {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }
r = requests.get(url, headers = headers)
objID = r.json()
myid = objID['id']
print("My ID: ", myid)
time.sleep(1)

#Getting List of guild channels
url = 'https://discordapp.com/api/v6/users/@me/guilds'
headers = {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }
r = requests.get(url, headers = headers)
objA = r.json()
guildList = []
for guild in objA:
    guildList.append(guild['id'])
time.sleep(1)


#Getting List of DM channels
url = 'https://discordapp.com/api/users/@me/channels'
headers = {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }
r = requests.get(url, headers = headers)
objA = r.json()
channelList = []
for channel in objA:
    channelList.append(channel["id"])
time.sleep(1)


toBeDeleted =[]


print("Searching for messages in all guild channels")

for guild in guildList:
    offset = 0
    totalMessages = 99999999
    while offset <= totalMessages:
        url = 'https://discordapp.com/api/guilds/' +guild+ '/messages/search?author_id=' + myid + '&offset=' + str(offset)
        r = requests.get(url, headers = headers)
        objB = r.json()
        totalMessages = objB['total_results']
        for stuff in objB['messages']:
            for message in stuff:
                if 'hit' in message:
                    if message['author']['id'] == myid:
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
        if message['author']['id'] == myid:
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
                if message['author']['id'] == myid:
                    print(channel,message['id'])
                    toBeDeleted.append([channel,message['id']])
        messageList.sort()
        if not len(messageList) or tempvalue == messageList[0]:
            scrape = False
        time.sleep(.5)

def delete(channel,message,token):
    url = 'https://discordapp.com/api/channels/' + channel + '/messages/' + message
    headers = {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }
    r = requests.delete(url, headers = headers)
    if r.status_code == 204:
        print("Deleted ", channel, " ", message)
    time.sleep(.25)

print("You are about to delete ", len(toBeDeleted), "messages.")
if input("Proceed? y/n") == 'y':
    for message in toBeDeleted:
        delete(message[0],message[1],token)

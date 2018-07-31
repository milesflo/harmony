'''
disconnect.py
This script deletes every DM you have ever sent on discord
pip3 install requests

python3 disconnect.py

'''
import requests
import time


print("Enter your email address: ")
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

#Getting UserID
url = 'https://discordapp.com/api/users/@me'
headers = {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }
r = requests.get(url, headers = headers)
objID = r.json()
myid = objID['id']

#Getting List of DM channels
url = 'https://discordapp.com/api/users/@me/channels'
headers = {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }
r = requests.get(url, headers = headers)
objA = r.json()
channelList = []
for channel in objA:
	channelList.append(channel["id"])


def delete(channel,message,token):
	url = 'https://discordapp.com/api/channels/' + channel + '/messages/' + message['id']
	print(url)
	headers = {"Accept-Encoding": "gzip, deflate","Content-Type": "application/json","Authorization": token }
	r = requests.delete(url, headers = headers)
	print(r)
	time.sleep(.25)


#Deleting messages
for channel in channelList:
	messageList = []
	url = 'https://discordapp.com/api/channels/' +channel+ '/messages'
	r = requests.get(url, headers = headers)
	objB = r.json()
	for message in objB:
		messageList.append(message['id'])
		if message['author']['id'] == myid:
			delete(channel,message,token)

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
					delete(channel,message,token)
		messageList.sort()
		if not len(messageList) or tempvalue == messageList[0]:
			scrape = False

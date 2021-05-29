import datetime
import os
from random import randint
import requests
import uuid


BOT_TOKEN = ""


def getLastMsgID():
    while True:
        inputDate = input(
            '\nHow far back to you wan\'t to fetch your images?\nExample: 03/29/21\n> '
        )
        if len(inputDate) == 8:
            break
        else:
            print('\nPlease input a valid date!\n')
    [month, day, year] = inputDate.split('/')
    date = datetime.datetime(2000 + int(year), int(month), int(day))

    return int((date.timestamp() * 1000) - 1420070400000) << 22


def getChannelID():
    channelID = os.environ.get('DEFAULT_CHANNEL_ID')
    while not channelID:
        inputChannelID = input(
            '\nWhich channel do you wan\'t to pull from?\nPlease enter the channel\'s ID\n> ')
        if len(inputChannelID) > 16:
            channelID = inputChannelID
        else:
            print('Please input a valid channel ID!\n')

    return channelID


def fetchMessages(channelID, lastMsgID):
    messages = []
    reqLen = 100
    reqCount = 1
    while reqLen == 100:
        url = f'https://discordapp.com/api/channels/{channelID}/messages?limit=100'
        if int(lastMsgID) > 0:
            url += f'&after={lastMsgID}'
        pulledMsgs = requests.get(
            url, headers={'Authorization': 'Bot ' + BOT_TOKEN}).json()
        lastMsgID = pulledMsgs[0]['id']
        reqLen = len(pulledMsgs)
        messages.append(pulledMsgs)
        print(f'[Req {reqCount}] Pulled {reqLen} messages!')
        reqCount += 1

    return [x for y in messages for x in y]


def parseImages(messages):
    images = []
    for message in messages:
        for attachment in message['attachments']:
            
                if attachment['width'] and attachment['height']:
                    print(attachment['url'])
                    response = requests.get(attachment['url'])
                    if response.status_code == 200:
                        with open(f"./pictures/{uuid.uuid4()}.jpg", 'wb') as f:
                            f.write(response.content)
                    images.append({
                        'url': attachment['url'],
                        'size': (attachment['width'], attachment['height'])
                    })
            


    maxImages = 500
    if len(images) > maxImages:
        images = images[-maxImages:]
        print(f'{len(images)} images found - only {maxImages} are being used!\n')
    else:
        print(f'{len(images)} images found!\n')

    return images



if __name__ == "__main__":
    if not BOT_TOKEN:
        print('Please add a BOT_TOKEN to your .env!')
        quit()

    lastMsgID = getLastMsgID()
    channelID = getChannelID()

    print('\nPulling messages from Discord...')
    messages = fetchMessages(channelID, lastMsgID)
    print(f'\nPulled {len(messages)} messages total!')

    images = parseImages(messages)

    print('★ Please consider starring the repository here: https://github.com/tfich/auto-collage\n')
    print('★ Edited by @clippedbypass \n')
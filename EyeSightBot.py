# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 12:02:40 2021

@author: ng_zh
"""
import requests
import datetime
import time

url = "https://app.acuityscheduling.com/schedule.php"
BotToken = '' #Insert Telegram Bot Token here


querystring = {"action":"showCalendar","fulldate":"1","owner":"20159891","template":"weekly"}

payload = "type=17382669&calendar=4550202&skip=true&options%255Bqty%255D=1&options%255BnumDays%255D=5&ignoreAppointment=&appointmentType=17382669&calendarID="
headers = {
    "cookie": "device_id=7b7300ae-011b-4001-a61d-6f2c5b799cdc; PHPSESSID=9qdchcouq8o65tpoj1r2g2g6ju",
    "authority": "app.acuityscheduling.com",
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "origin": "https://app.acuityscheduling.com",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://app.acuityscheduling.com/schedule.php?owner=20159891&appointmentType=17382669",
    "accept-language": "en-US,en;q=0.9"
}

def telegram_bot_sendtext(bot_message):

        bot_token = BotToken
        bot_chatID = '730459670'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        bot_chatID2 = "170022593"
        send_text2 = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID2 + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        response = requests.get(send_text2)
        return response.json()

def GetLatestTime():
    bot_token = BotToken
    send_text = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
    response = requests.get(send_text)
    
    return int(response.text.split('"date":')[-1].split(',"text"')[0])


def CheckOnline(LatestTime):
    bot_token = BotToken
    send_text = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
    response = requests.get(send_text)
    
    Time = int(response.text.split('"date":')[-1].split(',"text"')[0])
    if(Time != LatestTime):
        bot_message = "I am running"
        bot_chatIDs = [] #Insert Telegram ChatID here
        for IDs in bot_chatIDs:
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + IDs + '&parse_mode=Markdown&text=' + bot_message
            requests.get(send_text)
        return Time
    return LatestTime

PreviousDate = ''
LatestTime = GetLatestTime()
while(1):
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    Dates = response.text.replace('\n\n', '').split('\t\t\t\t\t')
    NewList = []
    for i in Dates:
        if(i.startswith('<div class="form-inline">')):
            NewList.append(i)
    
    Date = NewList[0].split('value="')[1].split('" id')[0].split(" ")[0]
    Day = datetime.datetime.strptime(Date, "%Y-%m-%d").strftime('%A')
    Time = NewList[0].split('value="')[1].split('" id')[0].split(" ")[1]

    if(PreviousDate != Date):
        ToSend = "Earliest Date: {Date}, {Day}, {Time}".format(Date = Date, Day = Day,  Time = Time)
        telegram_bot_sendtext(ToSend)
        PreviousDate = Date

    LatestTime = CheckOnline(LatestTime)
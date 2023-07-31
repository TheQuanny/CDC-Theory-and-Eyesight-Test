# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 12:02:40 2021

@author: ng_zh
"""
import requests
import datetime
from bs4 import BeautifulSoup
import time
import json
import pandas

def GetDates():
    GetPage = requests.get("https://www.cdc.com.sg:8443/wscdctestdate/api/testdate", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36" })
    Page = BeautifulSoup(GetPage, 'html.parser')

    BTT = Page.text.split('"Basic Theory Test"')[1].split('"date":')[1].split(',')[0]
    FTT = Page.text.split('"Final Theory Test"')[1].split('"date":')[1].split(',')[0]
    RTT = Page.text.split('"Class 2B Riding Theory Test"')[1].split('"date":')[1].split(',')[0]
    return BTT, FTT, RTT


def GetDay(Date):
    Date = Date.strip().strip('"')
    return datetime.datetime.strptime(Date, "%d %b %Y").strftime('%A')

def SendMessage(bot_message):
    bot_token = '' #Insert Telegram Bot Token here
    bot_chatIDs = [] #Insert Telegram ChatID here
    for IDs in bot_chatIDs:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + IDs + '&parse_mode=HTML&text=' + bot_message #&disable_web_page_preview=True
        requests.get(send_text)
    return None

def GetLatestTime():
    bot_token = '' #Insert Telegram Bot Token here
    LatestTime = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
    response = requests.get(LatestTime)
    
    return int(response.text.split('"date":')[-1].split(',"text"')[0])

def CheckOnline(LatestTime):
    bot_token = '' #Insert Telegram Bot Token here
    GetTime = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
    response = requests.get(GetTime)
    
    Time = int(response.text.split('"date":')[-1].split(',"text"')[0])
    if(Time != LatestTime):
        bot_message = "Script is Running"
        bot_chatIDs = [] #Insert Telegram ChatID here
        for IDs in bot_chatIDs:
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + IDs + '&parse_mode=HTML&text=' + bot_message #&disable_web_page_preview=True
            requests.get(send_text)
        return Time
    else:
        return LatestTime

if __name__ == "__main__":
    BTT, FTT, RTT = GetDates()
    LatestTime = CheckOnline(0)
    Message = "BTT: {BTT}, {BTTDay} \nFTT: {FTT}, {FTTDay} \nRTT: {RTT}, {RTTDay} ".format(BTT = BTT, BTTDay = GetDay(BTT), FTT = FTT, FTTDay = GetDay(FTT), RTT = RTT, RTTDay = GetDay(RTT))
    print(Message)
    SendMessage(Message)
    while(1):
        if(BTT != GetDates()[0]):
            BTT = GetDates()[0]
            Message = "BTT: {BTT}, {BTTDay} (Updated)\nFTT: {FTT}, {FTTDay} \nRTT: {RTT}, {RTTDay} ".format(BTT = BTT, BTTDay = GetDay(BTT), FTT = FTT, FTTDay = GetDay(FTT), RTT = RTT, RTTDay = GetDay(RTT))
            SendMessage(Message)
            
        if(FTT != GetDates()[1]):
            FTT = GetDates()[1]
            Message = "BTT: {BTT}, {BTTDay} \nFTT: {FTT}, {FTTDay}  (Updated)\nRTT: {RTT}, {RTTDay} ".format(BTT = BTT, BTTDay = GetDay(BTT), FTT = FTT, FTTDay = GetDay(FTT), RTT = RTT, RTTDay = GetDay(RTT))
            SendMessage(Message)
            
        if(RTT != GetDates()[2]):
            RTT = GetDates()[2]
            Message = "BTT: {BTT}, {BTTDay} \nFTT: {FTT}, {FTTDay} \nRTT: {RTT}, {RTTDay} (Updated)".format(BTT = BTT, BTTDay = GetDay(BTT), FTT = FTT, FTTDay = GetDay(FTT), RTT = RTT, RTTDay = GetDay(RTT))
            SendMessage(Message)
            
        LatestTime = CheckOnline(LatestTime)




import os
import requests
import pprint
import json
import time

def OnLoop(bot):
    fileName = os.path.join("files","streams.txt") 
    curGame = GetCurrentGame().strip()
    prevGame = GetMostRecentGame(fileName)
    print("cur="+curGame+",rec="+prevGame+"_")
    if prevGame != curGame:
        open(fileName,"a+").write(curGame.strip()+"\n")
    else:
        print("dup")

def GetMostRecentGame(f):
    lines = open(f,"r").readlines()
    if len(lines)>1:
       return lines[-1].strip()
    return ""
    

def GetCurrentGame():
    channel = open(os.path.join("files","twitch-id.txt")).read().strip()
    key = open(os.path.join("files","twitch-key.txt")).read().strip()
    url = "https://api.twitch.tv/kraken/channels/"+channel
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': key
    } 
    r = requests.get(url,headers=headers)
    data = json.loads(r.text)
    game = data["game"]
    if game == "Board Games"
        game = data["status"].split(':')[1]
    return game

while True:
    OnLoop()
    time.sleep(10)



import os

def loop():
    fileName = os.path.join("files","streams.txt") 
    curGame = GetCurrentGame().strip()
    latestGame = GetMostRecentGame(fileName)
    print("cur="+curGame+",rec="+latestGame+"_")
    if latestGame != curGame:
        open(fileName,"a+").write(curGame.strip()+"\n")
    else:
        print("dup")

def GetMostRecentGame(f):
    lines = open(f,"r").readlines()
    if len(lines)>1:
       return lines[-1].strip()
    return ""
    

def GetCurrentGame():
    return input("Enter Game:  ")



while True:
    loop()

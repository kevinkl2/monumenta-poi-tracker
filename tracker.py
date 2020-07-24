import time
from os import system, name
import os
import re
import datetime
import json
from dotenv import load_dotenv

# POI name, reset time
poiStore = {}

poiList = ["Azacor's Mansion",
            "Weeping Wormwood",
            "Consecrated Grounds",
            "Igor's Laboratory",
            "Mapleroot Town",
            "Hallowed Hedges",
            "Flooded Foyer",
            "The Undergrowth",
            "Collapsing Tower",
            "Waterfall Island"
            # "Nameless Ruins",
            # "Whispering Woods"
            ]

def clear():   
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')

def updateStore(name, line):
    try:
        if ("minutes" in line) and ("seconds" in line):
            pattern = r"\[(.*?)\] .* in (.+?) minutes and (.+?) seconds"
            matches = re.findall(pattern, line)
            timestamp, minutes, seconds = matches[0]
        elif ("minute" in line) and ("seconds" in line):
            pattern = r"\[(.*?)\] .* in (.+?) minute and (.+?) seconds"
            matches = re.findall(pattern, line)
            timestamp, minutes, seconds = matches[0]
        elif ("minutes" in line) and ("second" in line):
            pattern = r"\[(.*?)\] .* in (.+?) minutes and (.+?) second"
            matches = re.findall(pattern, line)
            timestamp, minutes, seconds = matches[0]
        elif ("minute" in line) and ("second" in line):
            pattern = r"\[(.*?)\] .* in (.+?) minute and (.+?) second"
            matches = re.findall(pattern, line)
            timestamp, minutes, seconds = matches[0]
        elif ("minutes" in line):
            pattern = r"\[(.*?)\] .* in (.+?) minutes"
            matches = re.findall(pattern, line)
            timestamp, minutes = matches[0]
            seconds = 0
        elif ("minute" in line):
            pattern = r"\[(.*?)\] .* in (.+?) minute"
            matches = re.findall(pattern, line)
            timestamp, minutes = matches[0]
            seconds = 0
        elif ("seconds" in line):
            pattern = r"\[(.*?)\] .* in (.+?) seconds"
            matches = re.findall(pattern, line)
            timestamp, seconds = matches[0]
            minutes = 0
        elif ("second" in line):
            pattern = r"\[(.*?)\] .* in (.+?) second"
            matches = re.findall(pattern, line)
            timestamp, seconds = matches[0]
            minutes = 0

        timestamp = datetime.datetime.strptime(timestamp, "%H:%M:%S")
        delta = datetime.timedelta(minutes=int(minutes), seconds=int(seconds))

        timestamp = timestamp+delta

        poiStore[name] = timestamp
        writeToFile()
    except Exception as e:
        print(e)

def printStore():
    currentTime = datetime.datetime.now().replace(year=1900,day=1,month=1)
    print(currentTime.strftime("%I:%M %p"))

    for poi in poiList:
        if poi in poiStore:
            if (poiStore[poi] < currentTime):
                color = "\x1b[0;30;42m"
                description = "TRUE"
            else:
                color = "\x1b[0;30;41m"
                description = "FALSE"
            print("{:>20}: {:>12} {}{:>12}\x1b[0m".format(poi, poiStore[poi].strftime("%I:%M %p"), color, description))

def parseLine(line, updated):
    for poi in poiList:
        if ("[main/INFO]: [CHAT] {}".format(poi) in line.rstrip()):
            if poi not in updated:
                updated.append(poi)
                updateStore(poi, line.rstrip())

def parseLogs():
    while(True):
        updated = []

        clear()
        printStore()

        for line in reversed(open(os.getenv("LATEST")).readlines()):
            parseLine(line, updated)

        time.sleep(1)

def datetimeConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def writeToFile():
    f = open("timers.json", "w")
    f.write(json.dumps(poiStore, default=datetimeConverter))
    f.close()

def readFromFile():
    try:
        f = open("timers.json", "r")
        poiFileData = json.loads(f.read())

        for poi in poiFileData:
            poiStore[poi] = datetime.datetime.strptime(poiFileData[poi], "%Y-%m-%d %H:%M:%S")  
    except Exception as e:
        print(e)

if __name__ == "__main__":
    load_dotenv()

    readFromFile()
    parseLogs()
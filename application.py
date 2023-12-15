import RPi.GPIO as GPIO
import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import rtc_ds3231 as rtc
import time
import database as db
from subprocess import call

import applicationxml as xml
import scr_watch as watchTime
import scr_settime as setTime
import scr_alarmtime as alarmTime
import scr_countertime as counterTime
import scr_userinfo as userInfo

scrSelect_ScrWatchAlarm = 0
scrSelect_ScrWatch = 1
scrSelect_ScrSetTime = 2
scrSelect_ScrAlarm = 3
scrSelect_ScrCounter = 4
scrSelect_ScrUserInfo = 5
scrSelect = 1

taskArrayIDPrevious = 0

userIdGlobal = "0"
userID = 0

def TouchIRQHandler(channel):
    global scrBackFlag
    xPos = 0
    yPos = 0
    posArray = [0] * 2
    if(touch.ReadCoordinates(posArray) == 1):	#reading touch coor completed
        xPos = int(posArray[0])
        yPos = int(posArray[1])
        
    if(xPos != 0 and yPos !=  0):
        print(xPos, yPos)
        
        if scrSelect == scrSelect_ScrWatch:
            watchTime.TouchHandler(xPos, yPos)
        elif scrSelect == scrSelect_ScrSetTime:
            setTime.TouchHandler(xPos, yPos)
        elif scrSelect == scrSelect_ScrAlarm:
            alarmTime.TouchHandler(xPos, yPos)
        elif scrSelect == scrSelect_ScrCounter:
            counterTime.TouchHandler(xPos, yPos)
        elif scrSelect == scrSelect_ScrUserInfo:
            userInfo.TouchHandler(xPos, yPos)

GPIO.add_event_detect(touch.TP_IRQ_PIN, GPIO.FALLING, callback=TouchIRQHandler, bouncetime=100)

#get alarm from database and give it to S3
def GetAlarmDataBase(userID):
    if userID == 0:
        alarmTime.ReceiveDataBase(1, 0, 0, 0)	#give to S3
        alarmTime.ReceiveDataBase(2, 0, 0, 0)
        alarmTime.ReceiveDataBase(3, 0, 0, 0)
    else:
        getData = db.firebase.database().child("users").child(userID).child("time").get()
        if (getData.each() == None):
            min1 = 0
            hour1 = 0
            check1 = 0
            min2 = 0
            hour2 = 0
            check2 = 0
            min3 = 0
            hour3 = 0
            check3 = 0
        else:
            for user in getData.each():
                if user.key() ==  "minute1":
                    min1 = int(user.val())
                elif user.key() ==  "hour1":
                    hour1 = int(user.val())
                elif user.key() ==  "minute2":
                    min2 = int(user.val())
                elif user.key() ==  "hour2":
                    hour2 = int(user.val())
                elif user.key() ==  "minute3":
                    min3 = int(user.val())
                elif user.key() ==  "hour3":
                    hour3 = int(user.val())
                elif user.key() ==  "alarm1":
                    check1 = int(user.val())
                elif user.key() ==  "alarm2":
                    check2 = int(user.val())
                elif user.key() ==  "alarm3":
                    check3 = int(user.val())
        
        print("Data alarm at GetAlarmDataBase")
        print(hour1, ":", min1, "=", check1)
        print(hour2, ":", min2, "=", check2)
        print(hour3, ":", min3, "=", check3)
        alarmTime.ReceiveDataBase(1, min1, hour1, check1)	#give to S3
        alarmTime.ReceiveDataBase(2, min2, hour2, check2)
        alarmTime.ReceiveDataBase(3, min3, hour3, check3)

def SetAlarmDataBase(userID, alarmNumber, minute, hour, status):
    if userID == 0:
        return 0
    if (alarmNumber == 1):
        getData = db.firebase.database().child("users").child("2019").child("time").child("alarm1").set(status)
        getData = db.firebase.database().child("users").child("2019").child("time").child("minute1").set(minute)
        getData = db.firebase.database().child("users").child("2019").child("time").child("hour1").set(hour)
    elif (alarmNumber == 2):
        getData = db.firebase.database().child("users").child("2019").child("time").child("alarm2").set(status)
        getData = db.firebase.database().child("users").child("2019").child("time").child("minute2").set(minute)
        getData = db.firebase.database().child("users").child("2019").child("time").child("hour2").set(hour)
    elif (alarmNumber == 3):
        getData = db.firebase.database().child("users").child("2019").child("time").child("alarm3").set(status)
        getData = db.firebase.database().child("users").child("2019").child("time").child("minute3").set(minute)
        getData = db.firebase.database().child("users").child("2019").child("time").child("hour3").set(hour)

#receive alarm update from S1 after alarm then give it to local and database
def TransAlarmToDataBaseAndLocal(timeArray, alarmType):   
    alarmTime.ReceiveDataBase(alarmType, timeArray[0], timeArray[1], timeArray[2])	#give to S3
    SetAlarmDataBase(userID, alarmType, timeArray[0], timeArray[1], timeArray[2])	#send to database

def TransAlarmFromS3ToS1():
    arrayBuffer = [0] * 9
    arrayBuffer = alarmTime.GiveAlarmLocal(arrayBuffer)
    return arrayBuffer

def SplitParagraph(paragraph):
    paragraphSplited = paragraph.split(":")
    return paragraphSplited

def GetTaskArray(userID):
    global taskArrayIDPrevious
    
    if userID == 0:
        return -1

    taskArray = []
    taskArrayIDNew = db.firebase.database().child("users").child(userID).child("tasks").child("check").get().val()
    if (taskArrayIDNew == None):	#no task found
        print("taskArrayIDNew = None")
        return -1
    else:
        if taskArrayIDNew != taskArrayIDPrevious:	#got new task
            getTask = db.firebase.database().child("users").child(userID).child("tasks").child("task").get().val()
            if (getTask == None):	#no task found
                print("getTask == None")
                return -1
            else:
                taskArray = SplitParagraph(getTask)
            taskArrayIDPrevious = taskArrayIDNew #update task ID
        else:	#no new tasks
            return 0
 
    return taskArray

def GetUserID():
    global userID
    getUserID = db.firebase.database().child("users").get()
    for user in  getUserID.each():
        if user.key() == userIdGlobal:
            userID = user.key()
            break
        else:
            userID = 0

#this funcion used by S5
def CheckLegitUserID(newID):
    global userID, userIdGlobal
    getUserID = db.firebase.database().child("users").get()
    for user in  getUserID.each():
        
        if user.key() == newID:		#id legit
            print(user.key())
            print(newID)
            userIdGlobal = user.key()
            userID = user.key()
            break
    
    if userIdGlobal != newID:
        return 0
    
    #told S1 to update data from new userID
    watchTime.MinutelyContactDataBase()

#this funcion used by S5
def GetStory(userID):
    if userID == 0:
        return 0
    
    getNameStory = db.firebase.database().child("users").child(userID).child("story").child("story").get().val()
    if (getNameStory == None):
        return 0
        #vspeak.VoiceSpeak("story's name not found")
    else:
        print("Story Name:", getNameStory)
        getStory = db.firebase.database().child("stories").child(getNameStory).get().val()
        if (getStory == None):
            return 0
        else:
            print(getStory)
            return getStory
            #vspeak.VoiceSpeak(getStory) 

#make a tunnel to give taskArray from S1 to S5, should not give directly from S1 to S5
def TunnelTaskArrayFromS1toS5():
    taskArrayTemp = watchTime.GiveTaskArray()
    return taskArrayTemp

#make a tunnel to give current alarm sound from S1 to S5, should not give directly from S1 to S5
def TunnelAlarmSoundFromS1toS5():
    currentSound = watchTime.GiveCurrentAlarmSound()
    return currentSound

#make a tunnel to give current alarm sound from S5 to S1, should not give directly from S5 to S1
def TunnelAlarmSoundFromS5toS1(currentMusicSetting):
    watchTime.ConfigAlarmSound(currentMusicSetting)

def ScrMain():
    global scrSelect
    global userID
    
    xml.DisplayTaskBar()
    xml.DisplayLowBar()
    xml.DisplayMenu()
    xml.DisplayWelcome()
    
    GetUserID()
    xml.DisplayUserID(userID)
    GetAlarmDataBase(userID)
    
    time.sleep(2)
    
    while True:
        if scrSelect == scrSelect_ScrWatch:
            watchTime.MainScreen()
        elif scrSelect == scrSelect_ScrSetTime:
            setTime.MainScreen()
        elif scrSelect == scrSelect_ScrAlarm:
            alarmTime.MainScreen()
        elif scrSelect == scrSelect_ScrCounter:
            counterTime.MainScreen()
        elif scrSelect == scrSelect_ScrUserInfo:
            userInfo.MainScreen()

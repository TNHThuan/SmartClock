import time
import rtc_ds3231 as rtc

from pygame import mixer
import voice_speak as vspeak

import application as app
import applicationxml as appxml
import scr_watchxml as xml

import music_alarm as music

scrBackFlag_OFF = 0
scrBackFlag_ON = 1
scrBackFlag = scrBackFlag_OFF #im global

alarmMin1 = 0
alarmMin2 = 0
alarmMin3 = 0
alarmHour1 = 0
alarmHour2 = 0
alarmHour3 = 0
alarmCheck1 = 0
alarmCheck2 = 0
alarmCheck3 = 0

alarmLockScreen = 0

arrayTask = []
taskRepeat = 0
MAX_REPEAT = 3

alarmMusicSound = music.cuteAlarm

def TouchHandler(xPos, yPos):
    global scrBackFlag
    global scrSelect
    global alarmLockScreen
    if alarmLockScreen == 0:	#not in alarm screen
        if ((xPos > (appxml.menu2X - appxml.menuSide) and xPos < (appxml.menu2X + appxml.menuSide))
            and (yPos > (appxml.menu2Y - appxml.menuSide) and yPos < (appxml.menu2Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrSetTime	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
        elif ((xPos > (appxml.menu3X - appxml.menuSide) and xPos < (appxml.menu3X + appxml.menuSide))
            and (yPos > (appxml.menu3Y - appxml.menuSide) and yPos < (appxml.menu3Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrAlarm	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
        elif ((xPos > (appxml.menu4X - appxml.menuSide) and xPos < (appxml.menu4X + appxml.menuSide))
            and (yPos > (appxml.menu4Y - appxml.menuSide) and yPos < (appxml.menu4Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrCounter	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
        elif ((xPos > (appxml.menu5X - appxml.menuSide) and xPos < (appxml.menu5X + appxml.menuSide))
            and (yPos > (appxml.menu5Y - appxml.menuSide) and yPos < (appxml.menu5Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrUserInfo	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
    else: #alarm screen happen, press anything to exit
        alarmLockScreen = 0
        app.scrSelect = app.scrSelect_ScrWatch
        scrBackFlag = scrBackFlag_ON

#---------------------------------------------------------------------
def ReceiveAlarmFromLocal():
    global alarmMin1, alarmHour1, alarmCheck1
    global alarmMin2, alarmHour2, alarmCheck2
    global alarmMin3, alarmHour3, alarmCheck3
    
    timeArray = app.TransAlarmFromS3ToS1()
    
    alarmMin1 = timeArray[0]
    alarmHour1 = timeArray[1]
    alarmCheck1 = timeArray[2]
    alarmMin2 = timeArray[3]
    alarmHour2 = timeArray[4]
    alarmCheck2 = timeArray[5]
    alarmMin3 = timeArray[6]
    alarmHour3 = timeArray[7]
    alarmCheck3 = timeArray[8]
    
def UpdateAlarmOnDataBase(alarmType):
    timeArray = [0] * 3
    if (alarmType == 1):
        timeArray[0] = alarmMin1
        timeArray[1] = alarmHour1
        timeArray[2] = alarmCheck1
    elif (alarmType == 2):
        timeArray[0] = alarmMin2
        timeArray[1] = alarmHour2
        timeArray[2] = alarmCheck2
    elif (alarmType == 3):
        timeArray[0] = alarmMin3
        timeArray[1] = alarmHour3
        timeArray[2] = alarmCheck3
    
    app.TransAlarmToDataBaseAndLocal(timeArray, alarmType)

#---------------------------------------------------------------------
def ConfigAlarmSound(config):
    global alarmMusicSound
    
    if config == 1:
        alarmMusicSound = music.cuteAlarm
    elif config == 2:
        alarmMusicSound = music.beepBeep
    elif config == 3:
        alarmMusicSound = music.hurryUp
    elif config == 4:
        alarmMusicSound = music.super11
    elif config == 5:
        alarmMusicSound = music.japanis
    elif config == 6:
        alarmMusicSound = music.theTime

def GiveCurrentAlarmSound():
    if alarmMusicSound == music.cuteAlarm:
        return 1
    elif alarmMusicSound == music.beepBeep:
        return 2
    elif alarmMusicSound == music.hurryUp:
        return 3
    elif alarmMusicSound == music.super11:
        return 4
    elif alarmMusicSound == music.japanis:
        return 5
    elif alarmMusicSound == music.theTime:
        return 6

#---------------------------------------------------------------------
def ActionWhenAlarmOn():
    global alarmMusicSound
    global alarmLockScreen
    alarmLockScreen = 1
    
    mixer.init()
    sound = mixer.Sound(alarmMusicSound.link)
    playing = sound.play()
    
    xml.DisplayAlarmScreen()
    
    startTime = time.time()
    while scrBackFlag == scrBackFlag_OFF:
        endTime = time.time()
        if (endTime - startTime > alarmMusicSound.time):
            startTime = endTime
            playing = sound.play()

    playing.stop()
    appxml.DisplayTaskBar()
    appxml.DisplayMenu()
    xml.DisplayBackground()
    appxml.DisplayLowBar()

def CheckIfAlarm(minNow, hourNow):
    global alarmMin1, alarmHour1, alarmCheck1
    global alarmMin2, alarmHour2, alarmCheck2
    global alarmMin3, alarmHour3, alarmCheck3
    
    if (alarmCheck1 == 1 and alarmMin1 == minNow and alarmHour1 == hourNow):
        alarmCheck1 = 0
        ActionWhenAlarmOn()
        UpdateAlarmOnDataBase(1)	#update alarm 1
    
    elif (alarmCheck2 == 1 and alarmMin2 == minNow and alarmHour2 == hourNow):
        alarmCheck2 = 0
        ActionWhenAlarmOn()
        UpdateAlarmOnDataBase(2)	#update alarm 2
        
    elif (alarmCheck3 == 1 and alarmMin3 == minNow and alarmHour3 == hourNow):
        alarmCheck3 = 0
        ActionWhenAlarmOn()
        UpdateAlarmOnDataBase(3)	#update alarm 3

#---------------------------------------------------------------------
def CheckTaskArray(minNow, hourNow):
    global arrayTask, taskRepeat

    totalPackageTask = len(arrayTask) // 3
    for i in range(totalPackageTask):
        if(hourNow == int(arrayTask[i*3]) and minNow == int(arrayTask[i*3+1])):
            vspeak.VoiceSpeak(arrayTask[i*3+2])
            taskRepeat += 1
            if (taskRepeat == MAX_REPEAT):	#disable this task
                arrayTask[i*3] = -1
                arrayTask[i*3+1] = -1
                arrayTask[i*3+2] = -1

def GiveTaskArray():	#give this arrayTask for Main App to transmit to S5. Should not give S5 arrayTask directly
    global arrayTask
    return arrayTask

#---------------------------------------------------------------------
def MinutelyContactDataBase():
    global arrayTask, taskRepeat
    
    app.GetAlarmDataBase(app.userID)
    ReceiveAlarmFromLocal()
    
    arrayTaskTemp = app.GetTaskArray(app.userID)
    if (arrayTaskTemp == -1):	#no task found
        arrayTask = [-1] * 3
    elif (arrayTaskTemp != 0):	#task found
        arrayTask = arrayTaskTemp
        
    print("minutely task:", arrayTask)

def MainScreen():
    global scrBackFlag
    global scrSelect
    scrBackFlag = scrBackFlag_OFF	#reset exit flag
    
    MinutelyContactDataBase()
    
    xml.DisplayMenu()
    xml.DisplayBackground()
    xml.DisplayStaticText()
    
    startTimeContactDataBase = time.time()
    startTimeDelay = 0
    while scrBackFlag == scrBackFlag_OFF:	#waiting for exit flag
        endTimeContectDataBase = time.time()
        if (endTimeContectDataBase - startTimeContactDataBase >= 59):	#minutely contact with database
            MinutelyContactDataBase()
            startTimeContactDataBase = endTimeContectDataBase
        
        
        endTimeDelay = time.time()
        if (endTimeDelay - startTimeDelay >= 1):	#1 seccond passed
            startTimeDelay = endTimeDelay
            
            #get the time and display it
            rtc.GetTime()
            xml.DisplayDymTime(rtc.DS3231_TimeNow.min, rtc.DS3231_TimeNow.hour,
                        rtc.DS3231_TimeNow.date, rtc.DS3231_TimeNow.month, rtc.DS3231_TimeNow.year);	#get the time from DS3231
            
            #check if alarm
            CheckIfAlarm(rtc.DS3231_TimeNow.min, rtc.DS3231_TimeNow.hour)
            
            #check if got task
            CheckTaskArray(rtc.DS3231_TimeNow.min, rtc.DS3231_TimeNow.hour)
            
    xml.DisplayResetMenu()

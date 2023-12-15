import RPi.GPIO as GPIO
import time

import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import rtc_ds3231 as rtc

import application as app
import applicationxml as appxml
import scr_alarmtimexml as xml

scrBackFlag_OFF = 0
scrBackFlag_ON = 1
scrBackFlag = scrBackFlag_OFF #im global

BUTTON_RESET = 0
BUTTON_CHECK1 = 1
BUTTON_HOUR1 = 2
BUTTON_MIN1 = 3
BUTTON_CHECK2 = 4
BUTTON_HOUR2 = 5
BUTTON_MIN2 = 6
BUTTON_CHECK3 = 7
BUTTON_HOUR3 = 8
BUTTON_MIN3 = 9
buttonType = BUTTON_RESET

BUTTON_OFF = 0
BUTTON_ON = 1
buttonUp = BUTTON_OFF
buttonDown = BUTTON_OFF

pointerType = BUTTON_RESET
pointerValue = 0

setTimeAlarmMin1 = 0
setTimeAlarmHour1 = 0
setTimeAlarmCheck1 = 0
setTimeAlarmMin2 = 0
setTimeAlarmHour2 = 0
setTimeAlarmCheck2 = 0
setTimeAlarmMin3 = 0
setTimeAlarmHour3 = 0
setTimeAlarmCheck3 = 0

timeIdleStart = 0
timeIdleEnd = 0
timeIdleCount = 0
TIME_IDLE_COUNT = 59	#waiting for TIME_IDLE_COUNT if not touch

def IdleTouchInit():
    global timeIdleCount
    global timeIdleStart
    
    timeIdleCount = TIME_IDLE_COUNT
    timeIdleStart = time.time()

def IdleNotTouchCount():
    global timeIdleCount
    global scrBackFlag, scrSelect
    global timeIdleStart, timeIdleEnd
    
    timeIdleEnd = time.time()
    if(timeIdleEnd - timeIdleStart >= 1):	#waiting for 1 seccond
        timeIdleCount -= 1
        if(timeIdleCount < 0):	#have not touch for TIME_IDLE_COUNT seccond
            app.scrSelect = app.scrSelect_ScrWatch	#confirm scrWatchTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
            return 1   
        timeIdleStart = timeIdleEnd
    
    return 0

def TouchHandler(xPos, yPos):
    global scrBackFlag
    global scrSelect
    global buttonType, buttonUp, buttonDown
    global timeIdleCount
    
    if ((xPos > (appxml.menu1X - appxml.menuSide) and xPos < (appxml.menu1X + appxml.menuSide))
        and (yPos > (appxml.menu1Y - appxml.menuSide) and yPos < (appxml.menu1Y + appxml.menuSide))):
        
        app.scrSelect = app.scrSelect_ScrWatch	#confirm scrWatchTime
        scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
    elif ((xPos > (appxml.menu2X - appxml.menuSide) and xPos < (appxml.menu2X + appxml.menuSide))
        and (yPos > (appxml.menu2Y - appxml.menuSide) and yPos < (appxml.menu2Y + appxml.menuSide))):
        
        app.scrSelect = app.scrSelect_ScrSetTime	#confirm scrSetTime
        scrBackFlag = scrBackFlag_ON	#turn of exit flag
    
    elif ((xPos > (appxml.menu4X - appxml.menuSide) and xPos < (appxml.menu4X + appxml.menuSide))
        and (yPos > (appxml.menu4Y - appxml.menuSide) and yPos < (appxml.menu4Y + appxml.menuSide))):
        
        app.scrSelect = app.scrSelect_ScrCounter	#confirm scrSetTime
        scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
    elif ((xPos > (appxml.menu5X - appxml.menuSide) and xPos < (appxml.menu5X + appxml.menuSide))
        and (yPos > (appxml.menu5Y - appxml.menuSide) and yPos < (appxml.menu5Y + appxml.menuSide))):
        
        app.scrSelect = app.scrSelect_ScrUserInfo	#confirm scrSetTime
        scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
    if (xPos > 150 and xPos < 174) and (yPos > 85 and yPos < 109):
        buttonType = BUTTON_CHECK1
    elif (xPos > 15 and xPos < 63) and (yPos > 80 and yPos < 112):
        buttonType = BUTTON_HOUR1
    elif (xPos > 85 and xPos < 113) and (yPos > 80 and yPos < 112):
        buttonType = BUTTON_MIN1

    elif (xPos > 150 and xPos < 174) and (yPos > 135 and yPos < 159):
        buttonType = BUTTON_CHECK2
    elif (xPos > 15 and xPos < 63) and (yPos > 130 and yPos < 162):
        buttonType = BUTTON_HOUR2
    elif (xPos > 85 and xPos < 113) and (yPos > 130 and yPos < 162):
        buttonType = BUTTON_MIN2

    elif (xPos > 150 and xPos < 174) and (yPos > 185 and yPos < 210):
        buttonType = BUTTON_CHECK3
    elif (xPos > 15 and xPos < 63) and (yPos > 180 and yPos < 212):
        buttonType = BUTTON_HOUR3
    elif (xPos > 85 and xPos < 113) and (yPos > 180 and yPos < 212):
        buttonType = BUTTON_MIN3

    if (xPos > 200 and xPos < 300) and (yPos > 80 and yPos < 110):
        buttonUp = BUTTON_ON
    elif (xPos > 200 and xPos < 300) and (yPos > 190 and yPos < 220):
        buttonDown = BUTTON_ON
    
    timeIdleCount = TIME_IDLE_COUNT		#already touched, reset waiting

def ReceiveDataBase(alarmType, minute, hour, check):
    print("data at ReceiveDataBase")
    print(alarmType, minute, hour, check)
    global setTimeAlarmMin1, setTimeAlarmHour1, setTimeAlarmCheck1
    global setTimeAlarmMin2, setTimeAlarmHour2, setTimeAlarmCheck2
    global setTimeAlarmMin3, setTimeAlarmHour3, setTimeAlarmCheck3
    
    if(alarmType == 1):
        setTimeAlarmMin1 = minute
        setTimeAlarmHour1 = hour
        setTimeAlarmCheck1 = check
    elif(alarmType == 2):
        setTimeAlarmMin2 = minute
        setTimeAlarmHour2 = hour
        setTimeAlarmCheck2 = check
    elif(alarmType == 3):
        setTimeAlarmMin3 = minute
        setTimeAlarmHour3 = hour
        setTimeAlarmCheck3 = check



def AssignTimeType(pValue, pType):
    global setTimeAlarmMin1, setTimeAlarmHour1
    global setTimeAlarmMin2, setTimeAlarmHour2
    global setTimeAlarmMin3, setTimeAlarmHour3
    
    if (pType == BUTTON_MIN1):
        setTimeAlarmMin1 = pValue
        xml.DisplayTimeMin1(setTimeAlarmMin1)
    elif (pType == BUTTON_HOUR1):
        setTimeAlarmHour1 = pValue
        xml.DisplayTimeHour1(setTimeAlarmHour1)
        
    elif (pType == BUTTON_MIN2):
        setTimeAlarmMin2 = pValue
        xml.DisplayTimeMin2(setTimeAlarmMin2)
    elif (pType == BUTTON_HOUR2):
        setTimeAlarmHour2 = pValue
        xml.DisplayTimeHour2(setTimeAlarmHour2)
        
    elif (pType == BUTTON_MIN3):
        setTimeAlarmMin3 = pValue
        xml.DisplayTimeMin3(setTimeAlarmMin3)
    elif (pType == BUTTON_HOUR3):
        setTimeAlarmHour3 = pValue
        xml.DisplayTimeHour3(setTimeAlarmHour3)

def GiveAlarmLocal(timeArray):
    timeArray[0] = setTimeAlarmMin1
    timeArray[1] = setTimeAlarmHour1
    timeArray[2] = setTimeAlarmCheck1
    timeArray[3] = setTimeAlarmMin2
    timeArray[4] = setTimeAlarmHour2
    timeArray[5] = setTimeAlarmCheck2
    timeArray[6] = setTimeAlarmMin3
    timeArray[7] = setTimeAlarmHour3
    timeArray[8] = setTimeAlarmCheck3
    return timeArray

def MainScreen():
    global scrBackFlag
    scrBackFlag = scrBackFlag_OFF	#reset exit flag
    
    global setTimeAlarmMin1, setTimeAlarmHour1, setTimeAlarmCheck1
    global setTimeAlarmMin2, setTimeAlarmHour2, setTimeAlarmCheck2
    global setTimeAlarmMin3, setTimeAlarmHour3, setTimeAlarmCheck3
    
    global pointerType, pointerValue
    global buttonType, buttonUp, buttonDown
    
    print("ready for GetAlarmDataBase")
    app.GetAlarmDataBase(app.userID)
    
    xml.DisplayMenu()
    xml.DisplayBackground()
    xml.DisplayStaticAlarmTime(setTimeAlarmMin1, setTimeAlarmHour1, setTimeAlarmMin2, setTimeAlarmHour2, setTimeAlarmMin3, setTimeAlarmHour3)
    xml.DisplayButton()
    xml.DisplayCheckAlarm1(setTimeAlarmCheck1)
    xml.DisplayCheckAlarm2(setTimeAlarmCheck2)
    xml.DisplayCheckAlarm3(setTimeAlarmCheck3)
    
    IdleTouchInit()
    while scrBackFlag == scrBackFlag_OFF:	#waiting for exit flag
        if(IdleNotTouchCount()):
            break
        
        if(buttonType == BUTTON_MIN1):
            pointerType = BUTTON_MIN1
            pointerValue = setTimeAlarmMin1
            xml.DisplayTimePointer(pointerValue)
            buttonType = BUTTON_RESET #do not need auto display again
        elif(buttonType == BUTTON_HOUR1):
            pointerType = BUTTON_HOUR1
            pointerValue = setTimeAlarmHour1
            xml.DisplayTimePointer(pointerValue)
            buttonType = BUTTON_RESET #do not need auto display again
        
        elif(buttonType == BUTTON_MIN2):
            pointerType = BUTTON_MIN2
            pointerValue = setTimeAlarmMin2
            xml.DisplayTimePointer(pointerValue)
            buttonType = BUTTON_RESET #do not need auto display again
        elif(buttonType == BUTTON_HOUR2):
            pointerType = BUTTON_HOUR2
            pointerValue = setTimeAlarmHour2
            xml.DisplayTimePointer(pointerValue)
            buttonType = BUTTON_RESET #do not need auto display again
            
        elif(buttonType == BUTTON_MIN3):
            pointerType = BUTTON_MIN3
            pointerValue = setTimeAlarmMin3
            xml.DisplayTimePointer(pointerValue)
            buttonType = BUTTON_RESET #do not need auto display again
        elif(buttonType == BUTTON_HOUR3):
            pointerType = BUTTON_HOUR3
            pointerValue = setTimeAlarmHour3
            xml.DisplayTimePointer(pointerValue)
            buttonType = BUTTON_RESET #do not need auto display again
        
        elif(buttonType == BUTTON_CHECK1):
            if setTimeAlarmCheck1:
                setTimeAlarmCheck1 = 0
            else:
                setTimeAlarmCheck1 = 1
            xml.DisplayCheckAlarm1(setTimeAlarmCheck1)
            app.SetAlarmDataBase(app.userID, 1, setTimeAlarmMin1, setTimeAlarmHour1, setTimeAlarmCheck1)
            buttonType = BUTTON_RESET #do not need auto display again
        elif(buttonType == BUTTON_CHECK2):
            if setTimeAlarmCheck2:
                setTimeAlarmCheck2 = 0
            else:
                setTimeAlarmCheck2 = 1
            xml.DisplayCheckAlarm2(setTimeAlarmCheck2)
            app.SetAlarmDataBase(app.userID, 2, setTimeAlarmMin2, setTimeAlarmHour2, setTimeAlarmCheck2)
            buttonType = BUTTON_RESET #do not need auto display again
        elif(buttonType == BUTTON_CHECK3):
            if setTimeAlarmCheck3:
                setTimeAlarmCheck3 = 0
            else:
                setTimeAlarmCheck3 = 1
            xml.DisplayCheckAlarm3(setTimeAlarmCheck3)
            app.SetAlarmDataBase(app.userID, 3, setTimeAlarmMin3, setTimeAlarmHour3, setTimeAlarmCheck3)
            buttonType = BUTTON_RESET #do not need auto display again
        
        if(buttonUp == BUTTON_ON):
            print("pressed up")
            if (pointerType == BUTTON_MIN1 or pointerType == BUTTON_MIN2 or pointerType == BUTTON_MIN3):
                if pointerValue == 59:
                    pointerValue = 0
                else:
                    pointerValue += 1
            elif (pointerType == BUTTON_HOUR1 or pointerType == BUTTON_HOUR2 or pointerType == BUTTON_HOUR3):
                if pointerValue == 23:
                    pointerValue = 0
                else:
                    pointerValue += 1
            xml.DisplayTimePointer(pointerValue)
            AssignTimeType(pointerValue, pointerType)
            buttonUp = BUTTON_OFF	#reset button after click
        elif(buttonDown == BUTTON_ON):
            print("pressed down")
            if (pointerType == BUTTON_MIN1 or pointerType == BUTTON_MIN2 or pointerType == BUTTON_MIN3):
                if pointerValue == 0:
                    pointerValue = 59
                else:
                    pointerValue -= 1
            elif (pointerType == BUTTON_HOUR1 or pointerType == BUTTON_HOUR2 or pointerType == BUTTON_HOUR3):
                if pointerValue == 0:
                    pointerValue = 23
                else:
                    pointerValue -= 1
            xml.DisplayTimePointer(pointerValue)
            AssignTimeType(pointerValue, pointerType)
            buttonDown = BUTTON_OFF	#reset button after click
    
    #send to database again to make sure saved changed data
    app.SetAlarmDataBase(app.userID, 1, setTimeAlarmMin1, setTimeAlarmHour1, setTimeAlarmCheck1)
    app.SetAlarmDataBase(app.userID, 2, setTimeAlarmMin2, setTimeAlarmHour2, setTimeAlarmCheck2)
    app.SetAlarmDataBase(app.userID, 3, setTimeAlarmMin3, setTimeAlarmHour3, setTimeAlarmCheck3)
    xml.DisplayResetMenu()

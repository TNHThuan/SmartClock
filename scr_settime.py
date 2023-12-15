import RPi.GPIO as GPIO
import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import rtc_ds3231 as rtc
import time

import application as app
import applicationxml as appxml
import scr_settimexml as xml

scrBackFlag_OFF = 0
scrBackFlag_ON = 1
scrBackFlag = scrBackFlag_OFF #im global

SETTING_TIME = 0
SETTING_SEC = 1
SETTING_MIN = 2
SETTING_HOUR = 3
SETTING_DAY = 4
SETTING_DATE = 5
SETTING_MONTH = 6
SETTING_YEAR = 7
SETTING_OK = 8
SETTING_NONE = 9
settingType = SETTING_NONE	#time or day
chooseSetting = SETTING_NONE	#sec, min or hour...

BUTTON_OFF = 0
BUTTON_ON = 1
buttonUp = BUTTON_OFF
buttonDown = BUTTON_OFF


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
    global settingType, chooseSetting, buttonUp, buttonDown
    if ((xPos > (appxml.menu1X - appxml.menuSide) and xPos < (appxml.menu1X + appxml.menuSide))
        and (yPos > (appxml.menu1Y - appxml.menuSide) and yPos < (appxml.menu1Y + appxml.menuSide))):
        
        app.scrSelect = app.scrSelect_ScrWatch	#confirm scrWatchTime
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
    
    if (xPos > 210 and xPos < 312 and yPos > 75 and yPos < 115):	#pressed setting time
        chooseSetting = SETTING_TIME
        
    elif (xPos > 95 and xPos < 197 and yPos > 75 and yPos < 115):	#pressed setting date
        chooseSetting = SETTING_DAY
        
    elif (xPos > 11 and xPos < 77 and yPos > 75 and yPos < 115):	#pressed confirm
        chooseSetting = SETTING_OK
        
    elif (settingType == SETTING_TIME and (xPos > 210 and xPos < 260 and yPos > 165 and yPos < 185)):	#pressed sec
        chooseSetting = SETTING_SEC
        
    elif (settingType == SETTING_TIME and (xPos > 140 and xPos < 190 and yPos > 165 and yPos < 185)):	#pressed min
        chooseSetting = SETTING_MIN
        
    elif (settingType == SETTING_TIME and (xPos > 70 and xPos < 120 and yPos > 165 and yPos < 185)):	#pressed hour
        chooseSetting = SETTING_HOUR
     
    elif (settingType == SETTING_DAY and (xPos > 40 and xPos < 88 and yPos > 165 and yPos < 197)):	#pressed date
        chooseSetting = SETTING_DATE
    
    elif (settingType == SETTING_DAY and (xPos > 110 and xPos < 158 and yPos > 165 and yPos < 197)):	#pressed month
        chooseSetting = SETTING_MONTH
    
    elif (settingType == SETTING_DAY and (xPos > 190 and xPos < 276 and yPos > 165 and yPos < 197)):	#pressed year
        chooseSetting = SETTING_YEAR
        
    elif (xPos > 90 and xPos < 230) and (yPos > 135 and yPos < 160):	#press +
        buttonUp = BUTTON_ON
        
    elif (xPos > 90 and xPos < 230) and (yPos > 205 and yPos < 230):	#press -
        buttonDown = BUTTON_ON
    
    timeIdleCount = TIME_IDLE_COUNT		#already touched, reset waiting

def MainScreen():
    global scrBackFlag
    global settingType, chooseSetting
    global buttonUp, buttonDown
    
    settingType = SETTING_NONE	#time or day
    chooseSetting = SETTING_NONE	#sec, min or hour...
    scrBackFlag = scrBackFlag_OFF	#reset exit flag
    
    setTimeSec = 0; setTimeMin = 0; setTimeHour = 0
    setDate = 0; setMonth = 0; setYear = 0
    rtc.GetTime()  # get the time from DS3231
    setTimeSec = rtc.DS3231_TimeNow.sec
    setTimeMin = rtc.DS3231_TimeNow.min
    setTimeHour = rtc.DS3231_TimeNow.hour
    setDate = rtc.DS3231_TimeNow.date
    setMonth = rtc.DS3231_TimeNow.month
    setYear = rtc.DS3231_TimeNow.year

    xml.DisplayMenu()
    xml.DisplayBackground()
    xml.DisplayButton()
    
    IdleTouchInit()
    while scrBackFlag == scrBackFlag_OFF:
        if(IdleNotTouchCount()):
            break
        
        if chooseSetting == SETTING_TIME:
            xml.DisplayTime(setTimeSec, setTimeMin, setTimeHour)
            settingType = SETTING_TIME #Time setting section
            chooseSetting = SETTING_NONE #no need to auto display this again
        
        if chooseSetting == SETTING_SEC:
            if(buttonUp == BUTTON_ON):
                if setTimeSec == 59:
                    setTimeSec = 0
                else:
                    setTimeSec += 1
                buttonUp = BUTTON_OFF
            elif(buttonDown == BUTTON_ON):
                if setTimeSec == 0:
                    setTimeSec = 59
                else:
                    setTimeSec -= 1
                buttonDown = BUTTON_OFF
            xml.DisplaySec(setTimeSec)

        elif chooseSetting == SETTING_MIN:
            if(buttonUp == BUTTON_ON):
                if setTimeMin == 59:
                    setTimeMin = 0
                else:
                    setTimeMin += 1
                buttonUp = BUTTON_OFF
            elif(buttonDown == BUTTON_ON):
                if setTimeMin == 0:
                    setTimeMin = 59
                else:
                    setTimeMin -= 1
                buttonDown = BUTTON_OFF
            xml.DisplayMin(setTimeMin)

        elif chooseSetting == SETTING_HOUR:
            if(buttonUp == BUTTON_ON):
                if setTimeHour == 23:
                    setTimeHour = 0
                else:
                    setTimeHour += 1
                buttonUp = BUTTON_OFF
            elif(buttonDown == BUTTON_ON):
                if setTimeHour == 0:
                    setTimeHour = 23
                else:
                    setTimeHour -= 1
                buttonDown = BUTTON_OFF
            xml.DisplayHour(setTimeHour)
    
        elif chooseSetting == SETTING_DAY:
            xml.DisplayDay(setDate, setMonth, setYear)
            settingType = SETTING_DAY #Day setting section
            chooseSetting = SETTING_NONE #no need to auto display this again
            
        elif chooseSetting == SETTING_DATE:
            if(buttonUp == BUTTON_ON):
                if setDate == 31:
                    setDate = 0
                else:
                    setDate += 1
                buttonUp = BUTTON_OFF
            elif(buttonDown == BUTTON_ON):
                if setDate == 0:
                    setDate = 31
                else:
                    setDate -= 1
                buttonDown = BUTTON_OFF
            xml.DisplayDate(setDate)
            
        elif chooseSetting == SETTING_MONTH:
            if(buttonUp == BUTTON_ON):
                if setMonth == 12:
                    setMonth = 0
                else:
                    setMonth += 1
                buttonUp = BUTTON_OFF
            elif(buttonDown == BUTTON_ON):
                if setMonth == 0:
                    setMonth = 12
                else:
                    setMonth -= 1
                buttonDown = BUTTON_OFF
            xml.DisplayMonth(setMonth)
            
        elif chooseSetting == SETTING_YEAR:
            if(buttonUp == BUTTON_ON):
                if setYear == 99:
                    setYear = 0
                else:
                    setYear += 1
                buttonUp = BUTTON_OFF
            elif(buttonDown == BUTTON_ON):
                if setYear == 0:
                    setYear = 99
                else:
                    setYear -= 1
                buttonDown = BUTTON_OFF
            xml.DisplayYear(setYear)
            
        elif chooseSetting == SETTING_OK:	#confirm and exit
            rtc.SetTime(setTimeSec, setTimeMin, setTimeHour, setDate, setMonth, setYear)
            chooseSetting = SETTING_NONE #no need to auto confirm this again
    
    xml.DisplayResetMenu()
import time
from pygame import mixer

import application as app
import applicationxml as appxml
import scr_countertimexml as xml

scrBackFlag_OFF = 0
scrBackFlag_ON = 1
scrBackFlag = scrBackFlag_OFF #im global

FRAGMENT_SETTING = 0     #fragment setting
FRAGMENT_RUNNING = 1     #fragment running
FRAGMENT_PAUSE = 2       #fragment pause
FRAGMENT_ALARM = 3       #fragment alarm
counterFragment = FRAGMENT_SETTING

SETTING_NOTHING = 0     #button in setting fragment
SETTING_SEC = 1
SETTING_MIN = 2
SETTING_HOUR = 3
SETTING_START = 4
SETTING_RESET = 5

RUNNING_PAUSE = 1       #button in setting running
RUNNING_STOP = 2

PAUSE_UNPAUSE = 0       #button in setting pause
PAUSE_STOP = 2

ALARM_WAIT = 0
ALARM_REPLAY = 1

selectButton = SETTING_NOTHING
counterSecond = 0
counterMinute = 0
counterHour = 0

BUTTON_OFF = 0
BUTTON_ON = 1
buttonUp = BUTTON_OFF
buttonDown = BUTTON_OFF

timeIdleStart = 0
timeIdleEnd = 0
timeIdleCount = 0
TIME_IDLE_COUNT = 59 #waiting for TIME_IDLE_COUNT if not touch

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
    global selectButton, buttonUp, buttonDown
    global counterFragment
    
    if counterFragment == FRAGMENT_SETTING:     #only handle touch in fragment setting
        if ((xPos > (appxml.menu1X - appxml.menuSide) and xPos < (appxml.menu1X + appxml.menuSide))
            and (yPos > (appxml.menu1Y - appxml.menuSide) and yPos < (appxml.menu1Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrWatch	#confirm scrWatchTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
        elif ((xPos > (appxml.menu2X - appxml.menuSide) and xPos < (appxml.menu2X + appxml.menuSide))
            and (yPos > (appxml.menu2Y - appxml.menuSide) and yPos < (appxml.menu2Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrSetTime	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
        
        elif ((xPos > (appxml.menu3X - appxml.menuSide) and xPos < (appxml.menu3X + appxml.menuSide))
            and (yPos > (appxml.menu3Y - appxml.menuSide) and yPos < (appxml.menu3Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrAlarm	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
            
        elif ((xPos > (appxml.menu5X - appxml.menuSide) and xPos < (appxml.menu5X + appxml.menuSide))
            and (yPos > (appxml.menu5Y - appxml.menuSide) and yPos < (appxml.menu5Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrUserInfo	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag

        if (xPos > 218 and xPos < 304) and (yPos > 70 and yPos < 134):
            print("SETTING_SEC")
            selectButton = SETTING_SEC
        elif (xPos > 118 and xPos < 204) and (yPos > 70 and yPos < 134):
            print("SETTING_MIN")
            selectButton = SETTING_MIN
        elif (xPos > 17 and xPos < 113) and (yPos > 70 and yPos < 134):
            print("SETTING_HOUR")
            selectButton = SETTING_HOUR
        elif (xPos > 90 and xPos < 230) and (yPos > 185 and yPos < 225):
            selectButton = SETTING_START
        elif (xPos > 110 and xPos < 150) and (yPos > 140 and yPos < 180):
            buttonUp = BUTTON_ON
        elif (xPos > 170 and xPos < 210) and (yPos > 140 and yPos < 180):
            buttonDown = BUTTON_ON
        else:
            selectButton = SETTING_NOTHING

    elif counterFragment == FRAGMENT_RUNNING:   #only handle touch in fragment running
        if (xPos > 90 and xPos < 230) and (yPos > 140 and yPos < 180):  # pause button
            selectButton = RUNNING_PAUSE
        elif (xPos > 90 and xPos < 230) and (yPos > 185 and yPos < 225):  # stop button
            selectButton = RUNNING_STOP

    elif counterFragment == FRAGMENT_PAUSE:     #only handle touch in fragment pause
        if (xPos > 90 and xPos < 230) and (yPos > 140 and yPos < 180):  # unpause button
            selectButton = PAUSE_UNPAUSE
        elif (xPos > 90 and xPos < 230) and (yPos > 185 and yPos < 225):  # stop button
            selectButton = PAUSE_STOP
    
    elif counterFragment == FRAGMENT_ALARM:     #only handle touch in fragment alarm
        if (xPos > 90 and xPos < 230) and (yPos > 185 and yPos < 225):  # stop button
            selectButton = ALARM_REPLAY
            
    timeIdleCount = TIME_IDLE_COUNT

def TimeAdd(timeValue, timeType):
    if (timeType == SETTING_SEC or timeType == SETTING_MIN):
        if (timeValue == 59):
            timeValue = 0
        else:
            timeValue += 1
    elif (timeType == SETTING_HOUR):
        if (timeValue == 23):
            timeValue = 0
        else:
            timeValue += 1
    return timeValue

def TimeMinus(timeValue, timeType):
    if (timeType == SETTING_SEC or timeType == SETTING_MIN):
        if (timeValue == 0):
            timeValue = 59
        else:
            timeValue -= 1
    elif (timeType == SETTING_HOUR):
        if (timeValue == 0):
            timeValue = 23
        else:
            timeValue -= 1
    return timeValue

def PressedPause():
    global counterFragment
    
    counterFragment = FRAGMENT_PAUSE
    xml.DisplayButtonPlay()		#display button play
    print("pressed pause")
    print("selectButton", selectButton)
    print("counterFragment", counterFragment)
    while (selectButton == RUNNING_PAUSE):  #waiting until unpause
        pass

    counterFragment = FRAGMENT_RUNNING  #get back to running fragment
    xml.DisplayButtonPause()    #display after unpause
    
def TimeUp():
    global counterFragment, selectButton
    counterFragment = FRAGMENT_ALARM	#is on alarm fragment
    selectButton = ALARM_WAIT	#make sure to waiting for press replay
    
    xml.DisplayTimeUp()
    xml.DisplayReplay()
    
    mixer.init()
    sound = mixer.Sound('/home/pi/Documents/alarmcounter.wav')
    playing = sound.play()
    
    startTime = time.time()
    while selectButton == ALARM_WAIT:
        endTime = time.time()
        if(endTime - startTime > 6):
            startTime = endTime
            playing = sound.play()
    
    playing.stop()
    return 0

def CounterRunning(counterSecond, counterMinute, counterHour):
    xml.DisplayColon()
    xml.DisplayButtonPause()
    xml.DisplayButtonStop()

    counterSecond -= 1	#minus 1, cause 60s => 59 to 0
    startTimeSecondDelay = 0
    for iHour in range (counterHour, -1, -1):
        for iMinute in range (counterMinute, -1, -1):
            for iSecond in range (counterSecond, -1, -1):
                while True:
                    endTimeSecondDelay = time.time()
                    if endTimeSecondDelay - startTimeSecondDelay >= 1:  #1 second passed
                        xml.DisplaySec(iSecond)
                        xml.DisplayMin(iMinute)
                        xml.DisplayHour(iHour)
                        startTimeSecondDelay = endTimeSecondDelay
                        break

                    #pressed pause at running fragment
                    if (selectButton == RUNNING_PAUSE):  
                        PressedPause()

                    #pressed stop at running fragment
                    #RUNNING_STOP is the same with PAUSE_STOP so do not worry about stop when pause
                    if (selectButton == RUNNING_STOP):
                        return 0

            counterSecond = 59
        counterMinute = 59 
    TimeUp()

def MainScreen():
    global scrBackFlag
    global scrSelect
    scrBackFlag = scrBackFlag_OFF	#reset exit flag

    global counterFragment, selectButton
    global buttonUp, buttonDown
    global counterSecond, counterMinute, counterHour
    
    xml.DisplayMenu()
    xml.DisplayBackground()
    xml.DisplayStaticText()
    xml.DisplayButtonUpDown()
    xml.DisplayButtonStart()
    
    IdleTouchInit()
    while scrBackFlag == scrBackFlag_OFF:	#waiting for exit flag
        if(IdleNotTouchCount()):
            break

        if selectButton == SETTING_SEC:
            if buttonUp == BUTTON_ON:
                buttonUp = BUTTON_OFF
                counterSecond = TimeAdd(counterSecond, selectButton)
            if buttonDown == BUTTON_ON:
                buttonDown = BUTTON_OFF
                counterSecond = TimeMinus(counterSecond, selectButton)
            xml.DisplaySecBlank()
            xml.DisplaySec(counterSecond)

        elif selectButton == SETTING_MIN:
            if buttonUp == BUTTON_ON:
                buttonUp = BUTTON_OFF
                counterMinute = TimeAdd(counterMinute, selectButton)
            if buttonDown == BUTTON_ON:
                buttonDown = BUTTON_OFF
                counterMinute = TimeMinus(counterMinute, selectButton)
            xml.DisplayMinBlank()
            xml.DisplayMin(counterMinute)

        elif selectButton == SETTING_HOUR:
            if buttonUp == BUTTON_ON:
                buttonUp = BUTTON_OFF
                counterHour = TimeAdd(counterHour, selectButton)
            if buttonDown == BUTTON_ON:
                buttonDown = BUTTON_OFF
                counterHour = TimeMinus(counterHour, selectButton)
            xml.DisplayHourBlank()
            xml.DisplayHour(counterHour)

        elif selectButton == SETTING_START:
            counterFragment = FRAGMENT_RUNNING  #go into running fragment
            CounterRunning(counterSecond, counterMinute, counterHour)
            selectButton = SETTING_RESET    #need reset
        
        #reset display after came back from running fragment
        elif selectButton == SETTING_RESET:
            selectButton = SETTING_NOTHING  #no need to auto reset again
            counterFragment = FRAGMENT_SETTING  #ready for setting fragment
            
            print(counterHour, ":", counterMinute, ":", counterSecond)
            xml.DisplaySec(counterSecond)
            xml.DisplayMin(counterMinute)
            xml.DisplayHour(counterHour)
            xml.DisplayCleanButton()
            xml.DisplayButtonUpDown()
            xml.DisplayButtonStart()

    xml.DisplayResetMenu()
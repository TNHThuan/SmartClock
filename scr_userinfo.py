import time

from pygame import mixer
import voice_speak as vspeak

import music_alarm as music

import application as app
import applicationxml as appxml
import scr_userinfoxml as xml

scrBackFlag_OFF = 0
scrBackFlag_ON = 1
scrBackFlag = scrBackFlag_OFF #im global

SELECT_NOTHING = 0
SELECT_USER = 1
SELECT_MUSIC = 2
SELECT_STORY = 3
SELECT_TASKS = 4
selectButton = SELECT_NOTHING

FRAGMENT_NORMAL = 1
FRAGMENT_MUSIC = 2
FRAGMENT_USER = 3
screenFragment = FRAGMENT_NORMAL

currentMusicSetting = 0

MUSIC_NOTHING = 0
MUSIC_1 = 1
MUSIC_2 = 2
MUSIC_3 = 3
MUSIC_4 = 4
MUSIC_5 = 5
MUSIC_6 = 6
#exit music fragment, do not change this define to 0
MUSIC_EXIT = 7

playingSound = 0	#this thing will make a music (going to mixer)

USER_0 = 0; USER_1 = 1; USER_2 = 2; USER_3 = 3; USER_4 = 4
USER_5 = 5; USER_6 = 6; USER_7 = 7; USER_8 = 8; USER_9 = 9
USER_ENTER = 10; USER_DELETE = 11; USER_EXIT = 12; USER_NOTHING = 13

frameForNumber = ""
quantityInFrame = 0
totalString = "0000"

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
    global selectButton, screenFragment

    if screenFragment == FRAGMENT_NORMAL:
        if ((xPos > (appxml.menu1X - appxml.menuSide) and xPos < (appxml.menu1X + appxml.menuSide))
            and (yPos > (appxml.menu1Y - appxml.menuSide) and yPos < (appxml.menu1Y + appxml.menuSide))):
            
            app.scrSelect = app.scrSelect_ScrWatch	#confirm scrSetTime
            scrBackFlag = scrBackFlag_ON	#turn of exit flag
            
        elif ((xPos > (appxml.menu2X - appxml.menuSide) and xPos < (appxml.menu2X + appxml.menuSide))
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
            
        if ((xPos > 28 and xPos < 147) and (yPos > 85 and yPos < 136)):
            selectButton = SELECT_USER
        elif ((xPos > 28 and xPos < 147) and (yPos > 161 and yPos < 212)):
            selectButton = SELECT_MUSIC
        elif ((xPos > 173 and xPos < 291) and (yPos > 85 and yPos < 136)):
            selectButton = SELECT_STORY
        elif ((xPos > 173 and xPos < 291) and (yPos > 161 and yPos < 212)):
            selectButton = SELECT_TASKS
    
    elif screenFragment == FRAGMENT_MUSIC:
        if ((xPos > 189 and xPos < 204) and (yPos > 89 and yPos < 108)):
            selectButton = MUSIC_1
        elif ((xPos > 189 and xPos < 204) and (yPos > 112 and yPos < 131)):
            selectButton = MUSIC_2
        elif ((xPos > 189 and xPos < 204) and (yPos > 135 and yPos < 154)):
            selectButton = MUSIC_3
        elif ((xPos > 189 and xPos < 204) and (yPos > 158 and yPos < 177)):
            selectButton = MUSIC_4
        elif ((xPos > 189 and xPos < 204) and (yPos > 181 and yPos < 200)):
            selectButton = MUSIC_5
        elif ((xPos > 189 and xPos < 204) and (yPos > 204 and yPos < 223)):
            selectButton = MUSIC_6
        elif not((xPos > 173 and xPos < 296) and (yPos > 66 and yPos < 227)):
            selectButton = MUSIC_EXIT
    
    elif screenFragment == FRAGMENT_USER:
        if ((xPos > 188 and xPos < 218) and (yPos > 76 and yPos < 106)):
            selectButton = USER_1
        elif ((xPos > 221 and xPos < 251) and (yPos > 76 and yPos < 106)):
            selectButton = USER_2
        elif ((xPos > 255 and xPos < 281) and (yPos > 76 and yPos < 106)):
            selectButton = USER_3
        elif ((xPos > 188 and xPos < 218) and (yPos > 113 and yPos < 143)):
            selectButton = USER_4
        elif ((xPos > 221 and xPos < 251) and (yPos > 113 and yPos < 143)):
            selectButton = USER_5
        elif ((xPos > 255 and xPos < 281) and (yPos > 113 and yPos < 143)):
            selectButton = USER_6
        elif ((xPos > 188 and xPos < 218) and (yPos > 150 and yPos < 180)):
            selectButton = USER_7
        elif ((xPos > 221 and xPos < 251) and (yPos > 150 and yPos < 180)):
            selectButton = USER_8
        elif ((xPos > 255 and xPos < 281) and (yPos > 150 and yPos < 180)):
            selectButton = USER_9
        elif ((xPos > 188 and xPos < 218) and (yPos > 187 and yPos < 217)):
            selectButton = USER_DELETE
        elif ((xPos > 221 and xPos < 251) and (yPos > 187 and yPos < 217)):
            selectButton = USER_0
        elif ((xPos > 255 and xPos < 281) and (yPos > 187 and yPos < 217)):
            selectButton = USER_ENTER
            
        elif not((xPos > 173 and xPos < 296) and (yPos > 66 and yPos < 227)):
            print("exit")
            selectButton = USER_EXIT
    
    timeIdleCount = TIME_IDLE_COUNT


#-------------------------------------------------------------
def PressedStory():
    story = app.GetStory(app.userID)
    if story == 0:
        vspeak.VoiceSpeak("story's name not found")
        return 0
    else:
        vspeak.VoiceSpeak(story)
        return 1


#-------------------------------------------------------------
#ask Main App give todoList from S1, should not take todoList directly from S1 to S5
def PressedTasks():
    todoList = app.TunnelTaskArrayFromS1toS5()
    
    totalPackageTask = len(todoList) // 3
    if (totalPackageTask == 1 and todoList[0] == -1):
        vspeak.VoiceSpeak("Task not found")
    for i in range(totalPackageTask):
        if(todoList[i*3] == -1):
            pass
        else:
            text = "at " + todoList[i*3] + " hour " + todoList[i*3 + 1] + " minute " + todoList[i*3 + 2]
            vspeak.VoiceSpeak(text)


#-------------------------------------------------------------
def ShowAllMusicOff():
    xml.DisplayMusic1Off()
    xml.DisplayMusic2Off()
    xml.DisplayMusic3Off()
    xml.DisplayMusic4Off()
    xml.DisplayMusic5Off()
    xml.DisplayMusic6Off()
    
def ShowCurrentMusic(currentMusic):
    if currentMusic == 1:
        xml.DisplayMusic1On()
    elif currentMusic == 2:
        xml.DisplayMusic2On()
    elif currentMusic == 3:
        xml.DisplayMusic3On()
    elif currentMusic == 4:
        xml.DisplayMusic4On()
    elif currentMusic == 5:
        xml.DisplayMusic5On()
    elif currentMusic == 6:
        xml.DisplayMusic6On()

def TakeCurrentMusic():
    currentSound = app.TunnelAlarmSoundFromS1toS5()
    return currentSound

def SendCurrentMusic(currentMusicSetting):
    app.TunnelAlarmSoundFromS5toS1(currentMusicSetting)

def ShowMusicList():
    global currentMusicSetting
    global screenFragment
    screenFragment = FRAGMENT_MUSIC		#go to music fragment

    xml.DisplayMusicList()
    xml.DisplayMusic1()
    xml.DisplayMusic2()
    xml.DisplayMusic3()
    xml.DisplayMusic4()
    xml.DisplayMusic5()
    xml.DisplayMusic6()
    
    ShowAllMusicOff()
    currentMusicSetting = TakeCurrentMusic()
    ShowCurrentMusic(currentMusicSetting)
    
def TryToStopSound():
    global playingSound
    try:
        playingSound.stop()
    except:
        pass

#sound on click - should need this thing ???
def RunSound(currentSound):
    global playingSound

    mixer.init()
    sound = mixer.Sound(music.musicArray[currentSound - 1].link)
    TryToStopSound()
    playingSound = sound.play()


def PressedMusic(music):
    global selectButton, currentMusicSetting
    
    selectButton = MUSIC_NOTHING	#reset cause no need to auto display again
    ShowAllMusicOff()
    currentMusicSetting = music
    ShowCurrentMusic(currentMusicSetting)
    
    SendCurrentMusic(music)		#send to S1
    RunSound(music)

def SelectMusic():
    global currentMusicSetting
    global selectButton
    selectButton = MUSIC_NOTHING	#reset touch, are in fragment Music
    
    while selectButton != MUSIC_EXIT:	#waiting for exit
        if selectButton == MUSIC_1:
            PressedMusic(1)
        elif selectButton == MUSIC_2:
            PressedMusic(2)
        elif selectButton == MUSIC_3:
            PressedMusic(3)
        elif selectButton == MUSIC_4:
            PressedMusic(4)
        elif selectButton == MUSIC_5:
            PressedMusic(5)
        elif selectButton == MUSIC_6:
            PressedMusic(6)
    
    TryToStopSound()
            
def ReturnToNormalFragment():
    global screenFragment
    screenFragment = FRAGMENT_NORMAL	#return to normal fragment
    
    xml.DisplayEraseFragment()
    xml.DisplayStory()
    xml.DisplayTasks()


#-------------------------------------------------------------
def ShowKeypad():
    global screenFragment
    screenFragment = FRAGMENT_USER		#go to music fragment
    
    xml.DisplayKeypad()
    xml.DisplayUserID("    ")

def AddNumberIntoString(number):
    global frameForNumber, quantityInFrame
    
    if (quantityInFrame < 4):
        frameForNumber += str(number)
        quantityInFrame += 1
    
    xml.DisplayUserID(frameForNumber)
    
def DeleteNumberInString():
    global frameForNumber, quantityInFrame
    
    frameForNumber = ""
    quantityInFrame = 0
    xml.DisplayUserID("    ")

def TESTINGADDNUMBER():		#delete this shit after complete keypad
    global selectButton
    AddNumberIntoString(2)
    time.sleep(1)
    AddNumberIntoString(0)
    time.sleep(1)
    AddNumberIntoString(1)
    time.sleep(1)
    AddNumberIntoString(9)
    time.sleep(1)
    selectButton = USER_ENTER
    
def UpdateUserID(newID):    
    if (app.CheckLegitUserID(newID) == 0):
        print("ID not found!")
        vspeak.VoiceSpeak("ID not found")
    else:
        print("Updated user ID")
        vspeak.VoiceSpeak("Updated user ID")

def PickNumber():
    global frameForNumber
    global selectButton
    selectButton = USER_NOTHING	#reset touch, are in fragment User
    
    while selectButton != USER_EXIT:
        #TESTINGADDNUMBER()
        if selectButton == USER_0:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(0)
        elif selectButton == USER_1:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(1)
        elif selectButton == USER_2:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(2)
        elif selectButton == USER_3:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(3)
        elif selectButton == USER_4:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(4)
        elif selectButton == USER_5:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(5)
        elif selectButton == USER_6:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(6)
        elif selectButton == USER_7:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(7)
        elif selectButton == USER_8:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(8)
        elif selectButton == USER_9:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            AddNumberIntoString(9)
        elif selectButton == USER_DELETE:
            selectButton = USER_NOTHING		#reset cause no need to auto add this number again
            DeleteNumberInString()
        elif selectButton == USER_ENTER:
            selectButton = USER_EXIT
            UpdateUserID(frameForNumber)
            DeleteNumberInString()		#clean number in string whatever ID legit or not

    
def MainScreen():
    global scrBackFlag
    scrBackFlag = scrBackFlag_OFF	#reset exit flag
    global selectButton, screenFragment
    
    xml.DisplayMenu()
    xml.DisplayBackground()
    xml.DisplayUser()
    if (app.userID != 0): 
        xml.DisplayUserID(app.userID)
    xml.DisplayMusic()
    xml.DisplayStory()
    xml.DisplayTasks()
    
    IdleTouchInit()
    while scrBackFlag == scrBackFlag_OFF:	#waiting for exit flag
        if(IdleNotTouchCount()):
            break
        
        if (selectButton == SELECT_USER):
            selectButton = SELECT_NOTHING
            ShowKeypad()
            PickNumber()
            ReturnToNormalFragment()
            if(app.userID != 0):
                xml.DisplayUserID(app.userID)
            else:
                xml.DisplayUserID("    ")
            
        elif (selectButton == SELECT_MUSIC):
            selectButton = SELECT_NOTHING
            ShowMusicList()
            SelectMusic()
            ReturnToNormalFragment()
            
        elif (selectButton == SELECT_STORY):
            selectButton = SELECT_NOTHING
            PressedStory()
        elif (selectButton == SELECT_TASKS):
            selectButton = SELECT_NOTHING
            PressedTasks()
        
        
    xml.DisplayResetMenu()
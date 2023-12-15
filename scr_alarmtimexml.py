import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import lcd_image as image

import applicationxml as appxml

def DisplayBackground():
    driver.DrawImage(0, 62, 320, 169, image.background)
    
def DisplayMenu():
    driver.DrawImage(appxml.menu3X, appxml.menu3Y, appxml.menuSide, appxml.menuSide, image.menu3On)

def DisplayResetMenu():
    driver.DrawImage(appxml.menu3X, appxml.menu3Y, appxml.menuSide, appxml.menuSide, image.menu3Off)

def DisplayStaticAlarmTime(min1, hour1, min2, hour2, min3, hour3):
    driver.DrawImage(7, 80, 133, 40, image.textbase)
    gfx.DrawNum(hour1, 15, 80, color.WHITE, 4, 0x04f8) #0x0558
    gfx.DrawChar(':', 70, 80, color.WHITE, 4, 0x04f8)
    gfx.DrawNum(min1, 85, 80, color.WHITE, 4, 0x04f8)

    driver.DrawImage(7, 130, 133, 40, image.textbase)
    gfx.DrawNum(hour2, 15, 130, color.WHITE, 4, 0x04f8) 
    gfx.DrawChar(':', 70, 130, color.WHITE, 4, 0x04f8)
    gfx.DrawNum(min2, 85, 130, color.WHITE, 4, 0x04f8)

    driver.DrawImage(7, 180, 133, 40, image.textbase)
    gfx.DrawNum(hour3, 15, 180, color.WHITE, 4, 0x04f8)
    gfx.DrawChar(':', 70, 180, color.WHITE, 4, 0x04f8)
    gfx.DrawNum(min3, 85, 180, color.WHITE, 4, 0x04f8)

def DisplayButton():
    driver.DrawImage(200, 75, 100, 34, image.buttonup2)
    driver.DrawImage(200, 185, 100, 34, image.buttondown2)
    
def DisplayCheckAlarm1(alarm1):
    if alarm1:
        driver.DrawImage(150, 85, 24, 24, image.alarmon)
    else:
        driver.DrawImage(150, 85, 24, 24, image.alarmoff)

def DisplayCheckAlarm2(alarm2):
    if alarm2:
        driver.DrawImage(150, 135, 24, 24, image.alarmon)
    else:
        driver.DrawImage(150, 135, 24, 24, image.alarmoff)

def DisplayCheckAlarm3(alarm3):
    if alarm3:
        driver.DrawImage(150, 185, 24, 24, image.alarmon)
    else: 
        driver.DrawImage(150, 185, 24, 24, image.alarmoff)
        
def DisplayTimePointer(pValue):
    gfx.DrawNum(pValue, 200, 110, color.WHITE, 9, 0x0558)
    
def DisplayTimeMin1(value):
    gfx.DrawNum(value, 85, 80, color.WHITE, 4, 0x04f8)

def DisplayTimeHour1(value):
    gfx.DrawNum(value, 15, 80, color.WHITE, 4, 0x04f8)

def DisplayTimeMin2(value):
    gfx.DrawNum(value, 85, 130, color.WHITE, 4, 0x04f8)

def DisplayTimeHour2(value):
    gfx.DrawNum(value, 15, 130, color.WHITE, 4, 0x04f8)

def DisplayTimeMin3(value):
    gfx.DrawNum(value, 85, 180, color.WHITE, 4, 0x04f8)

def DisplayTimeHour3(value):
    gfx.DrawNum(value, 15, 180, color.WHITE, 4, 0x04f8)
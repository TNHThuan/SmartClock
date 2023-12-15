import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import lcd_image as image

import applicationxml as appxml

def DisplayBackground():
    driver.DrawImage(0, 62, 320, 169, image.background)
    
def DisplayMenu():
    driver.DrawImage(appxml.menu1X, appxml.menu1Y, appxml.menuSide, appxml.menuSide, image.menu1On)

def DisplayResetMenu():
    driver.DrawImage(appxml.menu1X, appxml.menu1Y, appxml.menuSide, appxml.menuSide, image.menu1Off)

def DisplayStaticText():
    gfx.DrawChar(':', 155, 80, color.WHITE, 9, 0x0558)
    gfx.DrawChar('/', 90, 180, color.WHITE, 4, 0x0558)
    gfx.DrawChar('/', 160, 180, color.WHITE, 4, 0x0558)
    gfx.DrawText("20", 180, 180, color.WHITE, 4, 0x0558)
    
def DisplayDymTime(minute, hour, date, month, year):
    gfx.DrawNum(minute, 200, 80, color.WHITE, 9, 0x0558);	#display min
    gfx.DrawNum(hour, 20, 80, color.WHITE, 9, 0x0558);	#display hour
    gfx.DrawNum(date, 40, 180, color.WHITE, 4, 0x0558);	#display date
    gfx.DrawNum(month, 110, 180, color.WHITE, 4, 0x0558);	#display month
    gfx.DrawNum(year, 228, 180, color.WHITE, 4, 0x0558);	#display year

def DisplayAlarmScreen():
    driver.FillScreen(color.RED)
    gfx.DrawText("ALARM!", 50, 70, color.YELLOW, 7, color.RED)
    gfx.DrawText("Press anything to continue", 5, 140, color.YELLOW, 2, color.RED)
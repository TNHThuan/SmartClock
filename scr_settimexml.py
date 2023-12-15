import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import lcd_image as image

import applicationxml as appxml

menuSide = 32
    
def DisplayMenu():
    driver.DrawImage(appxml.menu2X, appxml.menu2Y, appxml.menuSide, appxml.menuSide, image.menu2On)

def DisplayResetMenu():
    driver.DrawImage(appxml.menu2X, appxml.menu2Y, appxml.menuSide, appxml.menuSide, image.menu2Off)

def DisplayBackground():
    driver.DrawImage(0, 62, 320, 169, image.background)

def DisplayButton():
    driver.DrawImage(11, 75, 66, 40, image.buttonok)
    driver.DrawImage(95, 75, 102, 40, image.buttondate)
    driver.DrawImage(210, 75, 102, 40, image.buttonhour)
    driver.DrawImage(90, 135, 140, 24, image.buttonup1)
    driver.DrawImage(90, 205, 140, 24, image.buttondown1)
    
def DisplayTime(second, minute, hour):
    gfx.DrawFilledRectangleCoord(30, 168, 280, 195, 0x0558)  # clear
    gfx.DrawNum(hour, 70, 165, color.WHITE, 4, 0x0558)
    gfx.DrawChar(':', 125, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(minute, 140, 165, color.WHITE, 4, 0x0558)
    gfx.DrawChar(':', 195, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(second, 210, 165, color.WHITE, 4, 0x0558)

def DisplayDay(date, month, year):
    gfx.DrawFilledRectangleCoord(30, 168, 280, 195, 0x0558)  # clear
    gfx.DrawNum(date, 40, 165, color.WHITE, 4, 0x0558)  # display date
    gfx.DrawChar('/', 90, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(month, 110, 165, color.WHITE, 4, 0x0558)  # display month
    gfx.DrawChar('/', 160, 165, color.WHITE, 4, 0x0558)
    gfx.DrawText("20", 180, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(year, 228, 165, color.WHITE, 4, 0x0558)  # display year

def DisplaySec(second):
    gfx.DrawText("  ", 210, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(second, 210, 165, color.WHITE, 4, 0x0558)

def DisplayMin(minute):
    gfx.DrawText("  ", 140, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(minute, 140, 165, color.WHITE, 4, 0x0558)
    
def DisplayHour(hour):
    gfx.DrawText("  ", 70, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(hour, 70, 165, color.WHITE, 4, 0x0558)

def DisplayDate(date):
    gfx.DrawText("  ", 40, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(date, 40, 165, color.WHITE, 4, 0x0558)
    
def DisplayMonth(month):
    gfx.DrawText("  ", 110, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(month, 110, 165, color.WHITE, 4, 0x0558)
    
def DisplayYear(year):
    gfx.DrawText("    ", 180, 165, color.WHITE, 4, 0x0558)
    gfx.DrawText("20", 180, 165, color.WHITE, 4, 0x0558)
    gfx.DrawNum(year, 228, 165, color.WHITE, 4, 0x0558)

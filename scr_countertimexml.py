import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import lcd_image as image

import applicationxml as appxml

def DisplayBackground():
    driver.DrawImage(0, 62, 320, 169, image.background)
    
def DisplayMenu():
    driver.DrawImage(appxml.menu4X, appxml.menu4Y, appxml.menuSide, appxml.menuSide, image.menu4On)

def DisplayResetMenu():
    driver.DrawImage(appxml.menu4X, appxml.menu4Y, appxml.menuSide, appxml.menuSide, image.menu4Off)
    
def DisplayStaticText():
    gfx.DrawText("00", 10, 70, color.WHITE, 8, 0x0558)  # Display hour
    gfx.DrawChar(':', 106, 85, color.WHITE, 5, 0x0558)
    gfx.DrawText("00", 116, 70, color.WHITE, 8, 0x0558)  # Display min
    gfx.DrawChar(':', 212, 85, color.WHITE, 5, 0x0558)
    gfx.DrawText("00", 223, 70, color.WHITE, 8, 0x0558)  # Display sec

def DisplayColon():
	gfx.DrawChar(':', 106, 85, color.WHITE, 5, 0x0558)
	gfx.DrawChar(':', 212, 85, color.WHITE, 5, 0x0558)

def DisplaySec(second):
	gfx.DrawNum(second, 223, 70, color.WHITE, 8, 0x0558)  # Display sec

def DisplayMin(minute):
	gfx.DrawNum(minute, 116, 70, color.WHITE, 8, 0x0558)  # Display sec

def DisplayHour(hour):
	gfx.DrawNum(hour, 10, 70, color.WHITE, 8, 0x0558)  # Display hour

def DisplaySecBlank():
	gfx.DrawText("  ", 223, 70, color.WHITE, 8, 0x0558)  # Display sec

def DisplayMinBlank():
	gfx.DrawText("  ", 116, 70, color.WHITE, 8, 0x0558)  # Display sec

def DisplayHourBlank():
	gfx.DrawText("  ", 10, 70, color.WHITE, 8, 0x0558)  # Display hour

def DisplayButtonUpDown():
	driver.DrawImage(110, 140, 40, 40, image.buttonup3)
	driver.DrawImage(170, 140, 40, 40, image.buttondown3)

def DisplayButtonStart():
	driver.DrawImage(90, 185, 140, 40, image.start)

def DisplayButtonStop():
	driver.DrawImage(90, 185, 140, 40, image.stop)

def DisplayButtonPause():
	driver.DrawImage(90, 140, 140, 40, image.pause)

def DisplayButtonPlay():
	driver.DrawImage(90, 140, 140, 40, image.play)
	
def DisplayCleanButton():
    gfx.DrawFilledRectangleCoord(90, 140, 230, 180, 0x0558)
    
def DisplayTimeUp():
    driver.DrawImage(90, 140, 140, 40, image.timeup)
    
def DisplayReplay():
    driver.DrawImage(90, 185, 140, 40, image.replay)
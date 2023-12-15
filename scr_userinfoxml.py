import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_touch as touch
import lcd32_color as color
import lcd_image as image

import applicationxml as appxml

def DisplayBackground():
    driver.DrawImage(0, 62, 320, 169, image.background)
    
def DisplayMenu():
    driver.DrawImage(appxml.menu5X, appxml.menu5Y, appxml.menuSide, appxml.menuSide, image.menu5On)

def DisplayResetMenu():
    driver.DrawImage(appxml.menu5X, appxml.menu5Y, appxml.menuSide, appxml.menuSide, image.menu5Off)
    
def DisplayUser():
    driver.DrawImage(28, 85, 119, 51, image.user)

def DisplayUserID(valueID):
    gfx.DrawText(valueID, 70, 92, 0x0558, 3, 0xef7d)
    
def DisplayMusic():
    driver.DrawImage(28, 161, 119, 51, image.music)
    
def DisplayStory():
    driver.DrawImage(173, 85, 119, 51, image.story)

def DisplayTasks():
    driver.DrawImage(173, 161, 119, 51, image.tasks)

def DisplayMusicList():
    driver.DrawImage(173, 66, 123, 161, image.musiclist)

def DisplayMusic1Off():
    driver.DrawImage(189, 89, 15, 19, image.musicoff)

def DisplayMusic2Off():
    driver.DrawImage(189, 112, 15, 19, image.musicoff)
    
def DisplayMusic3Off():
    driver.DrawImage(189, 135, 15, 19, image.musicoff)
    
def DisplayMusic4Off():
    driver.DrawImage(189, 158, 15, 19, image.musicoff)
    
def DisplayMusic5Off():
    driver.DrawImage(189, 181, 15, 19, image.musicoff)

def DisplayMusic6Off():
    driver.DrawImage(189, 204, 15, 19, image.musicoff)

def DisplayMusic1On():
    driver.DrawImage(189, 89, 15, 19, image.musicon)

def DisplayMusic2On():
    driver.DrawImage(189, 112, 15, 19, image.musicon)
    
def DisplayMusic3On():
    driver.DrawImage(189, 135, 15, 19, image.musicon)
    
def DisplayMusic4On():
    driver.DrawImage(189, 158, 15, 19, image.musicon)
    
def DisplayMusic5On():
    driver.DrawImage(189, 181, 15, 19, image.musicon)

def DisplayMusic6On():
    driver.DrawImage(189, 204, 15, 19, image.musicon)
    

def DisplayMusic1():
    driver.DrawImage(213, 94, 62, 11, image.music1)

def DisplayMusic2():
    driver.DrawImage(213, 117, 62, 12, image.music2)
    
def DisplayMusic3():
    driver.DrawImage(213, 140, 62, 12, image.music3)
    
def DisplayMusic4():
    driver.DrawImage(213, 163, 62, 12, image.music4)
    
def DisplayMusic5():
    driver.DrawImage(213, 186, 62, 12, image.music5)

def DisplayMusic6():
    driver.DrawImage(213, 209, 62, 12, image.music6)
    
def DisplayEraseFragment():
    driver.DrawImage(173, 66, 123, 161, image.erasekeypad)
    
def DisplayKeypad():
    driver.DrawImage(173, 66, 123, 161, image.keypad)
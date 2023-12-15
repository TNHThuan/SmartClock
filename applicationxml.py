import lcd32_driver as driver
import lcd32_gfx as gfx
import lcd32_color as color
import lcd_image as image

menuSide = 32

menu1X = 38 
menu1Y = 9
menu2X = 91
menu2Y = 9
menu3X = 145
menu3Y = 9
menu4X = 199
menu4Y = 9
menu5X = 253
menu5Y = 9

def DisplayTaskBar():
    driver.DrawImage(0, 0, 320, 62, image.taskbar)
    
def DisplayLowBar():
    driver.DrawImage(0, 231, 320, 9, image.lowbar)
    
def DisplayWelcome():
    driver.DrawImage(0, 62, 320, 169, image.welcome)
    
def DisplayMenu():
    driver.DrawImage(menu1X, menu1Y, menuSide, menuSide, image.menu1Off)
    driver.DrawImage(menu2X, menu2Y, menuSide, menuSide, image.menu2Off)
    driver.DrawImage(menu3X, menu3Y, menuSide, menuSide, image.menu3Off)
    driver.DrawImage(menu4X, menu4Y, menuSide, menuSide, image.menu4Off)
    driver.DrawImage(menu5X, menu5Y, menuSide, menuSide, image.menu5Off)

def DisplayUserID(userID):
    if userID != 0:
        gfx.DrawText(userID, 115, 160, color.WHITE, 4, 0x0558)

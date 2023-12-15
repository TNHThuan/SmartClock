import spidev
import RPi.GPIO as GPIO
import time
import copy

scrWidth = 320
scrHeight = 240

BURST_MAX_SIZE = 500

# GPIO Pin assignments
LCD_CS_PIN = 17
LCD_DC_PIN = 22
LCD_RST_PIN = 27

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LCD_CS_PIN, GPIO.OUT)
GPIO.setup(LCD_DC_PIN, GPIO.OUT)
GPIO.setup(LCD_RST_PIN, GPIO.OUT)

# SPI bus configuration
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 40000000

def LCD_PIN_SET(pin):
    GPIO.output(pin, GPIO.HIGH)

def LCD_PIN_RESET(pin):
    GPIO.output(pin, GPIO.LOW)

def SPISend(sendData):
    spi.xfer2([sendData])

def SPISendArray(sendData):
    spi.xfer2(sendData)

def WriteCmd(cmd):
    LCD_PIN_RESET(LCD_CS_PIN)
    LCD_PIN_RESET(LCD_DC_PIN)
    SPISend(cmd)
    LCD_PIN_SET(LCD_CS_PIN)

def WriteData(data):
    LCD_PIN_RESET(LCD_CS_PIN)
    LCD_PIN_SET(LCD_DC_PIN)
    SPISend(data)
    LCD_PIN_SET(LCD_CS_PIN)

def SetCursor(x1, y1, x2, y2):
    WriteCmd(0x2A)
    WriteData(x1 >> 8)
    WriteData(x1 & 0xFF)
    WriteData(x2 >> 8)
    WriteData(x2 & 0xFF)

    WriteCmd(0x2B)
    WriteData(y1 >> 8)
    WriteData(y1 & 0xFF)
    WriteData(y2 >> 8)
    WriteData(y2 & 0xFF)

    WriteCmd(0x2C)

def Init():
    LCD_PIN_RESET(LCD_RST_PIN)
    LCD_PIN_RESET(LCD_CS_PIN)
    LCD_PIN_SET(LCD_RST_PIN)

    WriteCmd(0x01)
    time.sleep(0.5)

    # Power control A
    WriteCmd(0xCB)
    WriteData(0x39)
    WriteData(0x2C)
    WriteData(0x00)
    WriteData(0x34)
    WriteData(0x02)

    # Power control B
    WriteCmd(0xCF)
    WriteData(0x00)
    WriteData(0xC1)
    WriteData(0x30)

    # Driver timing control A
    WriteCmd(0xE8)
    WriteData(0x85)
    WriteData(0x00)
    WriteData(0x78)

    # Driver timing control B
    WriteCmd(0xEA)
    WriteData(0x00)
    WriteData(0x00)

    # Power on sequence control
    WriteCmd(0xED)
    WriteData(0x64)
    WriteData(0x03)
    WriteData(0x12)
    WriteData(0x81)

    # Pump ratio control
    WriteCmd(0xF7)
    WriteData(0x20)

    # Power control, VRH[5:0]
    WriteCmd(0xC0)
    WriteData(0x23)

    # Power control, SAP[2:0];BT[3:0]
    WriteCmd(0xC1)
    WriteData(0x10)

    # VCM control
    WriteCmd(0xC5)
    WriteData(0x3E)
    WriteData(0x28)

    # VCM control 2
    WriteCmd(0xC7)
    WriteData(0x86)

    # Memory access control
    WriteCmd(0x36)
    WriteData(0x28)

    # Pixel format
    WriteCmd(0x3A)
    WriteData(0x55)

    # Frame ratio control, standard RGB color
    WriteCmd(0xB1)
    WriteData(0x00)
    WriteData(0x18)

    # Display function control
    WriteCmd(0xB6)
    WriteData(0x08)
    WriteData(0x82)
    WriteData(0x27)

    # 3Gamma function disable
    WriteCmd(0xF2)
    WriteData(0x00)

    # Gamma curve selected
    WriteCmd(0x26)
    WriteData(0x01)

    # Positive gamma correction
    WriteCmd(0xE0)
    WriteData(0x0F)
    WriteData(0x31)
    WriteData(0x2B)
    WriteData(0x0C)
    WriteData(0x0E)
    WriteData(0x08)
    WriteData(0x4E)
    WriteData(0xF1)
    WriteData(0x37)
    WriteData(0x07)
    WriteData(0x10)
    WriteData(0x03)
    WriteData(0x0E)
    WriteData(0x09)
    WriteData(0x00)

    # Negative gamma correction
    WriteCmd(0xE1)
    WriteData(0x00)
    WriteData(0x0E)
    WriteData(0x14)
    WriteData(0x03)
    WriteData(0x11)
    WriteData(0x07)
    WriteData(0x31)
    WriteData(0xC1)
    WriteData(0x48)
    WriteData(0x08)
    WriteData(0x0F)
    WriteData(0x0C)
    WriteData(0x31)
    WriteData(0x36)
    WriteData(0x0F)

    # Exit sleep
    WriteCmd(0x11)
    time.sleep(0.1)

    # Turn on display
    WriteCmd(0x29)

def DrawPixel(x, y, color):
    if x >= scrWidth or y >= scrHeight:
        return

    SetCursor(x, y, x+1, y+1)

    # COLOUR
    LCD_PIN_RESET(LCD_CS_PIN)
    LCD_PIN_SET(LCD_DC_PIN)
    SPISendArray([color >> 8, color])
    LCD_PIN_SET(LCD_CS_PIN)

def DrawFilRec(x, y, width, height, color):
    for i in range(y, height):
        for j in range(x, width):
            DrawPixel(j, i, color)

def DrawColourBurst(color, size):
    bufferSize = 0

    if (size * 2) < BURST_MAX_SIZE:
        bufferSize = size * 2
    else:
        bufferSize = BURST_MAX_SIZE

    LCD_PIN_RESET(LCD_CS_PIN)
    LCD_PIN_SET(LCD_DC_PIN)

    chiftedHigh = (color >> 8) & 0xFF
    chiftedLow = color & 0xFF
    burstBuffer = [0] * bufferSize
    for j in range(0, bufferSize, 2):
        burstBuffer[j] = chiftedHigh
        burstBuffer[j + 1] = chiftedLow

    sendingSize = size * 2
    sendingInBlock = sendingSize // bufferSize
    remainderFromBlock = sendingSize % bufferSize

    if sendingInBlock != 0:
        for j in range(0, sendingInBlock):
            #spi.xfer2(copy.copy(burstBuffer))
            SPISendArray(copy.copy(burstBuffer))

    if remainderFromBlock != 0:
        #spi.xfer2(copy.copy(burstBuffer[:remainderFromBlock]))
        SPISendArray(burstBuffer[:remainderFromBlock])

    LCD_PIN_SET(LCD_CS_PIN)


def FillScreen(color):
	SetCursor(0, 0, scrWidth, scrHeight)
	DrawColourBurst(color, scrWidth * scrHeight)

def DrawRectangle(xPos, yPos, width, height, color):
    if xPos >= scrWidth or yPos >= scrHeight:
        return
    if xPos + width - 1 >= scrWidth:
        width = scrWidth - xPos
    if yPos + height - 1 >= scrHeight:
        height = scrHeight - yPos
    SetCursor(xPos, yPos, xPos + width - 1, yPos + height - 1)
    DrawColourBurst(color, height * width)

def DrawHorizontalLine(xPos, yPos, width, color):
    if xPos >= scrWidth or yPos >= scrHeight:
        return
    if xPos + width - 1 >= scrWidth:
        width = scrWidth - xPos
    SetCursor(xPos, yPos, xPos + width - 1, yPos)
    DrawColourBurst(color, width)

def DrawVerticalLine(xPos, yPos, height, color):
    if xPos >= scrWidth or yPos >= scrHeight:
        return
    if yPos + height - 1 >= scrHeight:
        height = scrHeight - yPos
    SetCursor(xPos, yPos, xPos, yPos + height - 1)
    DrawColourBurst(color, height)

def DrawImage(xPos, yPos, width, height, imageArray):
    SetCursor(xPos, yPos, xPos+width-1, yPos+height-1)

    LCD_PIN_RESET(LCD_CS_PIN)
    LCD_PIN_SET(LCD_DC_PIN)
    
    TempSmallBuffer = [0] * BURST_MAX_SIZE
    counter = 0
    for i in range(width*height*2 // BURST_MAX_SIZE):
        for k in range(BURST_MAX_SIZE):
            TempSmallBuffer[k] = imageArray[counter + k]
        SPISendArray(TempSmallBuffer)
        counter += BURST_MAX_SIZE
    if((width*height*2 // BURST_MAX_SIZE) != 0):
        SPISendArray(imageArray[(width*height*2 // BURST_MAX_SIZE)*BURST_MAX_SIZE:width*height*2])
    
    LCD_PIN_SET(LCD_CS_PIN)




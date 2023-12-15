import lcd32_driver as driver
import lcd_6x8font as lcd_6x8font

def DrawFilledCircle(xPos, yPos, radius, color):
    xPnt = radius
    yPnt = 0
    xChange = 1 - (radius << 1)
    yChange = 0
    radiusError = 0

    while xPnt >= yPnt:
        for i in range(xPos - xPnt, xPos + xPnt + 1):
            driver.DrawPixel(i, yPos + yPnt, color)
            driver.DrawPixel(i, yPos - yPnt, color)
        for i in range(xPos - yPnt, xPos + yPnt + 1):
            driver.DrawPixel(i, yPos + xPnt, color)
            driver.DrawPixel(i, yPos - xPnt, color)

        yPnt += 1
        radiusError += yChange
        yChange += 2
        if (radiusError << 1) + xChange > 0:
            xPnt -= 1
            radiusError += xChange
            xChange += 2

def DrawHollowRectangleCoord(xStart, yStart, xEnd, yEnd, color):
    xLength = 0
    yLength = 0
    xNegative = 0
    yNegative = 0
    calcNegative = 0
    
    calcNegative = xEnd - xStart
    if calcNegative < 0:
        xNegative = 1
    calcNegative = 0
    
    calcNegative = yEnd - yStart
    if calcNegative < 0:
        yNegative = 1
    
    # DRAW HORIZONTAL!
    if not xNegative:
        xLength = xEnd - xStart
    else:
        xLength = xStart - xEnd
    driver.DrawHorizontalLine(xStart, yStart, xLength, color)
    driver.DrawHorizontalLine(xStart, yEnd, xLength, color)
    
    # DRAW VERTICAL!
    if not yNegative:
        yLength = yEnd - yStart
    else:
        yLength = yStart - yEnd
    driver.DrawVerticalLine(xStart, yStart, yLength, color)
    driver.DrawVerticalLine(xEnd, yStart, yLength, color)
    
    if xLength > 0 or yLength > 0:
        driver.DrawPixel(xEnd, yEnd, color)

def DrawFilledRectangleCoord(xStart, yStart, xEnd, yEnd, color):
    xLength = 0
    yLength = 0
    xNegative = 0
    yNegative = 0
    calcNegative = 0
    
    xTrue = 0
    yTrue = 0
    
    calcNegative = xEnd - xStart
    if calcNegative < 0:
        xNegative = 1
    calcNegative = 0
    
    calcNegative = yEnd - yStart
    if calcNegative < 0:
        yNegative = 1
    
    # DRAW HORIZONTAL!
    if not xNegative:
        xLength = xEnd - xStart
        xTrue = xStart
    else:
        xLength = xStart - xEnd
        xTrue = xEnd
    
    # DRAW VERTICAL!
    if not yNegative:
        yLength = yEnd - yStart
        yTrue = yStart
    else:
        yLength = yStart - yEnd
        yTrue = yEnd
    
    driver.DrawRectangle(xTrue, yTrue, xLength, yLength, color)

def DrawChar(textChar, xPos, yPos, textColour, textSize, bgColor):
    functionChar = ord(textChar)

    if functionChar < ord(' '):
        textChar = 0
    else:
        functionChar -= 32

    temp = [0] * lcd_6x8font.CHAR_WIDTH
    for k in range(lcd_6x8font.CHAR_WIDTH):
        temp[k] = lcd_6x8font.font_6x8[functionChar][k]

    # Draw pixels
    #if bgColor:
        #driver.DrawRectangle(xPos, yPos, lcd_6x8font.CHAR_WIDTH * textSize, lcd_6x8font.CHAR_HEIGHT * textSize, bgColor)

    for j in range(lcd_6x8font.CHAR_WIDTH):
        for i in range(lcd_6x8font.CHAR_HEIGHT):
            if temp[j] & (1 << i):
                if textSize == 1:
                    driver.DrawPixel(xPos + j, yPos + i, textColour)
                else:
                    driver.DrawRectangle(xPos + (j * textSize), yPos + (i * textSize), textSize, textSize, textColour)
            else:
                driver.DrawRectangle(xPos + (j * textSize), yPos + (i * textSize), textSize, textSize, bgColor)

def DrawText(textString, xPos, yPos, textColour, textSize, bgColor):
    while len(textString) > 0:
        DrawChar(textString[0], xPos, yPos, textColour, textSize, bgColor)
        xPos += lcd_6x8font.CHAR_WIDTH * textSize
        textString = textString[1:]

def DrawNum(num, xPos, yPos, textColour, textSize, bgColor):
    if num < 10:
        string = f"{num:02d}"
    else:
        string = str(num)

    DrawText(string, xPos, yPos, textColour, textSize, bgColor)



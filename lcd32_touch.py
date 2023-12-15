import RPi.GPIO as GPIO

TP_CLK_PIN	= 5
TP_CS_PIN	= 6
TP_MOSI_PIN	= 13
TP_MISO_PIN	= 19
TP_IRQ_PIN	= 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(TP_CLK_PIN, GPIO.OUT)
GPIO.setup(TP_CS_PIN, GPIO.OUT)
GPIO.setup(TP_MOSI_PIN, GPIO.OUT)
GPIO.setup(TP_MISO_PIN, GPIO.IN)
GPIO.setup(TP_IRQ_PIN, GPIO.IN)

CMD_RDY = 0x90
CMD_RDX = 0xD0

TOUCHPAD_NOT_PRESSED = 0
TOUCHPAD_PRESSED = 1

TOUCHPAD_DATA_OK = 1
TOUCHPAD_DATA_NOISY = 0

X_TRANSLATION = 12.8	#2^12 / 320 px
Y_TRANSLATION = 17.06	#2^12 / 240 px

SAMPLE_TIME = 50

def Read():
    value = 0

    for i in range(12):	#data receive only 12-bits
        value <<= 1

        GPIO.output(TP_CLK_PIN, GPIO.HIGH)
        GPIO.output(TP_CLK_PIN, GPIO.LOW)

        if GPIO.input(TP_MISO_PIN) != 0:
            value += 1

    return value

def Write(value):
    GPIO.output(TP_CLK_PIN, GPIO.LOW)
    for i in range(8):
        if (value & 0x80) != 0x00:
            GPIO.output(TP_MOSI_PIN, GPIO.HIGH)
        else:
            GPIO.output(TP_MOSI_PIN, GPIO.LOW)
            
        value <<= 1
        GPIO.output(TP_CLK_PIN, GPIO.HIGH)
        GPIO.output(TP_CLK_PIN, GPIO.LOW)

def ReadCoordinates(Coordinates):
    GPIO.output(TP_CLK_PIN, GPIO.HIGH)
    GPIO.output(TP_MOSI_PIN, GPIO.HIGH)
    GPIO.output(TP_CS_PIN, GPIO.HIGH)

    rawX, rawY = 0, 0
    totalX, totalY = 0, 0
    sampleForLoop = SAMPLE_TIME
    countedSample = 0

    GPIO.output(TP_CS_PIN, GPIO.LOW)	#start sending and receive

    while sampleForLoop > 0 and GPIO.input(TP_IRQ_PIN) == 0:
        Write(0xD0)	#turn on X line ADC channel
        rawY = Read()
        totalY += rawY

        Write(0x90)	#turn on Y line ADC channel
        rawX = Read()
        totalX += rawX

        sampleForLoop -= 1
        countedSample += 1

    GPIO.output(TP_CS_PIN, GPIO.HIGH)	#end sending and receive

    if countedSample == SAMPLE_TIME:
        totalX /= countedSample
        totalY /= countedSample

        Coordinates[0] = ((320 - (totalX / X_TRANSLATION)) - 15) * 1.15
        Coordinates[1] = ((240 - (totalY / Y_TRANSLATION)) - 15) * 1.15

        return TOUCHPAD_DATA_OK
    else:
        Coordinates[0] = 0
        Coordinates[1] = 0
        return TOUCHPAD_DATA_NOISY

def TouchpadPressed():
    if GPIO.input(TP_IRQ_PIN) == 0:
        return TOUCHPAD_PRESSED
    else:
        return TOUCHPAD_NOT_PRESSED

    
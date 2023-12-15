import lcd32_driver as driver
import lcd32_color as color
import time
import RPi.GPIO as GPIO
#import screen_activities as scract
import application as app
import lcd_image as image

driver.Init()
driver.FillScreen(color.CYAN)

#def SoftwareInterrupt(channel):
    #print("lmao here is interrupt")
    #GPIO.setup(SOFT_INTERRUPT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #time.sleep(1)

#SOFT_INTERRUPT	= 12
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(SOFT_INTERRUPT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(SOFT_INTERRUPT, GPIO.FALLING, callback=SoftwareInterrupt, bouncetime=10)

try:
    #scract.ScrMenu()
    app.ScrMain()
    '''
    a=0
    while True:
        a+=1
        print(a)
        if(a%3 == 0):
            print("Prepare for interrupt")
            GPIO.setup(SOFT_INTERRUPT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        time.sleep(1)'''
    print("DONE")
except KeyboardInterrupt:
    GPIO.cleanup()
    print("QUIT")
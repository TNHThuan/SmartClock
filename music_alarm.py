class MusicAlarm:
  def __init__(self, link, time):
    self.link = link
    self.time = time
    
cuteAlarm = MusicAlarm("/home/pi/Documents/alarm.wav", 15)
beepBeep = MusicAlarm("/home/pi/Documents/BeepBeep.wav", 3)
hurryUp = MusicAlarm("/home/pi/Documents/HurryUp.wav", 29)
super11 = MusicAlarm("/home/pi/Documents/Super11.wav", 23)
japanis = MusicAlarm("/home/pi/Documents/Japanis.wav", 25)
theTime = MusicAlarm("/home/pi/Documents/TheTime.wav", 28)
alarmCounter = MusicAlarm("/home/pi/Documents/alarmcounter.wav", 5)

musicArray = [cuteAlarm, beepBeep, hurryUp, super11, japanis, theTime]
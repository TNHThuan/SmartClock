import smbus
import time

DS3231_ADDRESS = 0x68

class DS3231_typedef:
    def __init__(self):
        self.sec = 0
        self.min = 0
        self.hour = 0
        self.day = 0
        self.date = 0
        self.month = 0
        self.year = 0

DS3231_TimeNow = DS3231_typedef()

def DEC2BCD(val):
    return int((val//10 * 16) + (val%10))

def BCD2DEC(val):
    return int((val//16 * 10) + (val%16))

def GetDay(date, month, year):
    JMD = (date + ((153 * (month + 12 * ((14 - month) // 12) - 3) + 2) // 5) +
           (365 * (year + 4800 - ((14 - month) // 12))) +
           ((year + 4800 - ((14 - month) // 12)) // 4) -
           ((year + 4800 - ((14 - month) // 12)) // 100) +
           ((year + 4800 - ((14 - month) // 12)) // 400) - 32045) % 7
    weekday = [2, 3, 4, 5, 6, 7, 1]
    return weekday[int(JMD)]

def SetTime(sec, minu, hour, date, month, year):
    DS3231_tranBuffer = [0] * 7
    DS3231_tranBuffer[0] = DEC2BCD(sec)
    DS3231_tranBuffer[1] = DEC2BCD(minu)
    DS3231_tranBuffer[2] = DEC2BCD(hour)

    DS3231_tranBuffer[3] = DEC2BCD(GetDay(date, month, year))
    DS3231_tranBuffer[4] = DEC2BCD(date)
    DS3231_tranBuffer[5] = DEC2BCD(month)
    DS3231_tranBuffer[6] = DEC2BCD(year)

    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(DS3231_ADDRESS, 0x00, DS3231_tranBuffer)
    bus.close()

def SetHour(sec, minu, hour):
    DS3231_tranBuffer = [0] * 3
    DS3231_tranBuffer[0] = DEC2BCD(sec)
    DS3231_tranBuffer[1] = DEC2BCD(minu)
    DS3231_tranBuffer[2] = DEC2BCD(hour)

    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(DS3231_ADDRESS, 0x00, DS3231_tranBuffer)
    bus.close()

def SetDay(date, month, year):
    DS3231_tranBuffer = [0] * 4
    DS3231_tranBuffer[0] = DEC2BCD(GetDay(date, month, year))
    DS3231_tranBuffer[1] = DEC2BCD(date)
    DS3231_tranBuffer[2] = DEC2BCD(month)
    DS3231_tranBuffer[3] = DEC2BCD(year)

    bus = smbus.SMBus(1)
    bus.write_i2c_block_data(DS3231_ADDRESS, 0x03, DS3231_tranBuffer)
    bus.close()

def GetTime():
    global DS3231_TimeNow
    DS3231_recBuffer = [0] * 7
    bus = smbus.SMBus(1)
    DS3231_recBuffer = bus.read_i2c_block_data(DS3231_ADDRESS, 0x00, 7)
    bus.close()
    time.sleep(0.001)
    DS3231_TimeNow.sec = BCD2DEC(DS3231_recBuffer[0])
    DS3231_TimeNow.min = BCD2DEC(DS3231_recBuffer[1])
    DS3231_TimeNow.hour = BCD2DEC(DS3231_recBuffer[2])
    DS3231_TimeNow.day = BCD2DEC(DS3231_recBuffer[3])
    DS3231_TimeNow.date = BCD2DEC(DS3231_recBuffer[4])
    DS3231_TimeNow.month = BCD2DEC(DS3231_recBuffer[5])
    DS3231_TimeNow.year = BCD2DEC(DS3231_recBuffer[6])
    
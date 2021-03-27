from machine import Pin, I2C
from lcd_api import lcdapi
from pico_i2c_lcd import I2cLcd
import utime
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c_ = I2C(0, sda=machine.Pin(20), scl=machine.Pin(21), freq=200000)
i2c_.scan()
lcd = I2cLcd(i2c_, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=200000)
i2c.scan()
DS3231_I2C_ADDR   = (0x68)
DS3231_REG_SEC    = (0x00)
DS3231_REG_MIN    = (0x01)
DS3231_REG_HOUR   = (0x02)

def HexToDec(data):
     data=int.from_bytes(data, "big")
     return (data//16) * 10 + (data%16)
    
def DecToHex(dat):
        return (dat//10) * 16 + (dat%10)
    
def yaz(saat_,dakika_,saniye_):
     saat_=DecToHex(saat_)
     dakika_=DecToHex(dakika_)
     saniye_=DecToHex(saniye_)
    
     i2c.scan()
     i2c.writeto(DS3231_I2C_ADDR,bytearray([0]))
     i2c.writeto_mem(DS3231_I2C_ADDR, DS3231_REG_SEC,bytes([saniye_]))
     i2c.writeto_mem(DS3231_I2C_ADDR, DS3231_REG_MIN,bytes([dakika_]))
     i2c.writeto_mem(DS3231_I2C_ADDR, DS3231_REG_HOUR,bytes([saat_]))
     
def oku():
    global saniye
    global dakika
    global saat
        
    i2c.writeto(DS3231_I2C_ADDR,bytearray([0]))
    saniye=i2c.readfrom_mem(DS3231_I2C_ADDR, DS3231_REG_SEC, 1)
    
    dakika=i2c.readfrom_mem(DS3231_I2C_ADDR, DS3231_REG_MIN, 1)
    
    saat=i2c.readfrom_mem(DS3231_I2C_ADDR, DS3231_REG_HOUR, 1)
    
    #saniye=int.from_bytes(saniye, "big")
    #saniye=(saniye//16) * 10 + (saniye%16)
    saniye=HexToDec(saniye)
    dakika=HexToDec(dakika)
    saat=HexToDec(saat)
#     dakika=int.from_bytes(dakika, "big")
#     dakika=(dakika//16) * 10 + (dakika%16)
    
#     saat=int.from_bytes(saat, "big")
#     saat=(saat//16) * 10 + (saat%16)
    
    saniye%=60
    dakika%=60
    saat%=24    
    
#     print(saniye)
#     print(dakika)
#     print(saokuat)
#yaz(20,25,0)    
# oku()

while True:
    
    oku()    
    saniye=str(saniye)
    dakika=str(dakika)
    saat=str(saat)
    lcd.move_to(0,0)
    lcd.putstr("SAAT: "+saat+":"+dakika+":"+saniye)
    utime.sleep_ms(1000)
    lcd.clear()
    
    
    
    
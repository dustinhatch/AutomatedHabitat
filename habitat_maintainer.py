#!/usr/bin/python
import sys
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import datetime
from RPLCD.gpio import CharLCD
from nanpy import (ArduinoApi, SerialManager)

def lcdWrite(line1, line2):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2)

def pinOn(pin):
    a.digitalWrite(pin, a.LOW)
    return True
    
def pinOff(pin):
    a.digitalWrite(pin, a.HIGH)
    return False
    
# Set pins
lcd = CharLCD(cols=16, rows=2, pin_rs=8, pin_e=10, pins_data=[16,18,22,24], numbering_mode=GPIO.BOARD)
dayPin=8
dayState=False
heatPin=7
heatState=False
humidityPin=10
humidityState=False
uvbPin=9
uvbState=False

try:
    connection=SerialManager()
    a=ArduinoApi(connection=connection)
    #lcdWrite("Arduino Status:", "Connected")
except:
    print("faled to connect")
    #lcdWrite("Arduino Status:", "Failed")

time.sleep(5)

# Set pinModes
a.pinMode(dayPin, a.OUTPUT)
a.digitalWrite(dayPin, a.HIGH)
a.pinMode(heatPin, a.OUTPUT)
a.digitalWrite(heatPin, a.HIGH)
a.pinMode(uvbPin, a.OUTPUT)
a.digitalWrite(uvbPin, a.HIGH)
a.pinMode(humidityPin, a.OUTPUT)
a.digitalWrite(humidityPin, a.HIGH)

# Begin loop
i=1
while i==1:
    h, temperature=Adafruit_DHT.read_retry(11, 8)
    humidity, t=Adafruit_DHT.read_retry(11, 7)
    if temperature != None:
        temperature=(temperature*1.8)+32
    timestamp=datetime.datetime.now()
    
    #lcdWrite('Temp: %d F' % temperature, 'Humidity: %d %%' % humidity)
    
    f=open("//home//pi//programs//sensor_readings.csv", "a")
    f.write(timestamp.strftime("%Y-%m-%d %H:%M"))
    f.write(",%s" % temperature)
    f.write(",%s\n" % humidity)
    f.close()
    
    if 8 <= timestamp.hour <= 19:
        if not dayState:
            dayState=pinOn(dayPin)
        if not uvbState:
            uvbState=pinOn(uvbPin)
        if temperature<80 and not heatState:
            heatState=pinOn(heatPin)
        elif temperature>85 and heatState:
            heatState=pinOff(heatPin)

    elif (timestamp.hour<=7 or timestamp.hour>=20):
        if dayState:
            dayState=pinOff(dayPin)
        if uvbState:
            uvbState=pinOff(uvbPin)
        if temperature<65 and not heatState:
            heatState=pinOn(heatPin)
        elif temperature>70 and heatState:
            heatState=pinOff(heatPin)

    if humidity>80 and humidityState:
       humidityState=pinOff(humidityPin)
    elif humidity<65 and not humidityState:
        humidityState=pinOn(humidityPin)
        
    time.sleep(60)

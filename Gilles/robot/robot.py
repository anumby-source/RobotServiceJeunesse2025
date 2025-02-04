###################################################################
#
#   Command car with ESP32-C3/ESPnow mini joystick
#
###################################################################

import os
import network
import espnow
from time import sleep_ms
from machine import Pin, UART
from dcMotor import dcMotor

# motors initialization
ml = dcMotor(pin1=7, pin2=6, pinEn=5)      # left motor
mr = dcMotor(pin1=0, pin2=1, pinEn=2)      # right motor
ml.duty_offset = 15
mr.duty_offset = 15
# led initialization
led = Pin(8, Pin.OUT)

def blink():
    for _ in range(8):
        led.off()
        sleep_ms(250)
        led.on()
        sleep_ms(250)
# UART initialization
u = UART(0, rx=Pin(20, Pin.IN), tx=Pin(21, Pin.OUT))

while not (u.any() == 7):  # wait for Maixbit wakeup
    sleep_ms(100)

print(u.read(u.any()))   # empty rx buffer
# espnow initialization
sta = network.WLAN(network.STA_IF) # A WLAN interface must be active
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)
dispAddr = b'\xa0\x85\xe3\x19\xb5\xdc' #  display panel Mac Address
e.add_peer(dispAddr)
joyAddr, msg = e.recv()   # wait for joystick wakeup
e.add_peer(joyAddr)
print(host, msg)
#
blink()
#
while True:
    if u.any():
        e.send(dispAddr, u.read())
        
    host, cmd = e.recv()
    try:
        exec(cmd)
    except:
        print(cmd)
        led.off()
        break
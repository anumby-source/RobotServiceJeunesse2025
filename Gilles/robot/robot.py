###################################################################
#
#   RSJ2025 : Robot code
#
###################################################################

import os
import network
import espnow
from time import sleep_ms, ticks_ms
from machine import Pin, UART
from dcMotor import dcMotor
from struct import pack

#
robot_num = 1
liste_pan = ['Paris', 'Auxerre', 'Lyon', 'Marseille']
# motors initialization
ml = dcMotor(pin1=5, pin2=6, pinEn=7, freq=10000)      # left motor
mr = dcMotor(pin1=0, pin2=1, pinEn=2, freq=10000)      # right motor
ml.duty_offset = 40
mr.duty_offset = 40
print("robot : motor init ok")
# led initialization
led = Pin(8, Pin.OUT)

# UART initialization
led.off()     # led on
u = UART(0, rx=Pin(20, Pin.IN), tx=Pin(21, Pin.OUT))
#
led.on()      # led off
sleep_ms(1000)
# espnow initialization
led.off()     # led on
sta = network.WLAN(network.STA_IF) # A WLAN interface must be active
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point
print("robot : WLAN init ok")
e = espnow.ESPNow()
e.active(True)
print("robot : espnow init ok")
# wait for joystick
joyAddr, msg = e.recv()   # wait for joystick wakeup
try:
    e.add_peer(joyAddr)
except:
    pass     # if joyAddr already in peer list
print(b"robot : message telecommande=" + msg)
# connect to base
baseAddr = b'$X|\x91\xe0\xd8' #  display panel Mac Address
try:
    e.add_peer(baseAddr)
except:
    pass      # if baseAddr already in peer list
#
led.on()      # led off
#
u.read(u.any())   # empty uart buffer
msg = b''
#
while True:
    if u.any():
        msg += u.read(u.any())
        if msg[-1] == 0x0a:  # last char = '\n'
            e.send(baseAddr, msg)
            print(msg)
            msg = b''       
    try:
        addr, cmd = e.recv()
#         print(cmd)
        exec(cmd)
    except:
        print(b"robot : error command:" + cmd)
        led.off()    # led on
        break
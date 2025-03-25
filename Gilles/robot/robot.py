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
baseAddr  = b'$X|\x91\xe0\xd8' #  base Mac Address
joyAddr   = b'\xa0\x85\xe3\x1aX\xb8'  #  joystick mac address

# motors initialization
ml = dcMotor(pin1=5, pin2=6, pinEn=7, freq=10000)      # left motor
mr = dcMotor(pin1=0, pin2=1, pinEn=2, freq=10000)      # right motor
ml.duty_offset = 40
mr.duty_offset = 40
print("robot : motor init ok")

# led initialization
led = Pin(8, Pin.OUT)
led.off()     # led on
sleep_ms(1000)
led.on()      # led off
print("robot : led init ok")

# UART initialization
u = UART(0, rx=Pin(20, Pin.IN), tx=Pin(21, Pin.OUT))
print("robot : UART init ok")

# espnow initialization
sta = network.WLAN(network.STA_IF) # A WLAN interface must be active
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point
print("robot : WLAN init ok")
e = espnow.ESPNow()
e.active(True)
print("robot : espnow init ok")

# add joystick and base to peers
try:
    e.add_peer(joyAddr)
except:
    pass         # if joyAddr already in peer list
print(b"robot : joystick address added")
# 
try:
    e.add_peer(baseAddr)
except:
    pass         # if baseAddr already in peer list
print(b"robot : base address added")
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
        addr, cmd = e.recv(0)
#         print(cmd)
        if addr == joyAddr:
            exec(cmd)
    except:
        print(b"robot : error command:" + cmd)
        led.off()    # led on
        break
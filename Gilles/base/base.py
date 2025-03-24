import sys
import network
import espnow
from time import sleep_ms
from machine import Pin
from mac_addr import robot_mac

# mac = b'$X|\x91\xe0\xd8'  # base MAC address
# espnow init
sta = network.WLAN(network.STA_IF)
sta.active(True)
e = espnow.ESPNow()
e.active(True)
print('espnow ok')
# led init
led = Pin(8, Pin.OUT)
led.on()    # led off
#
while True:
  addr, msg = e.recv(0)
  if addr:
      print("{}:{}".format(robot_mac[addr], msg.decode()))
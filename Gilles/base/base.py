import sys
import network
import espnow
from time import sleep_ms
from machine import Pin
from mac_addr import robot_mac

# mac = b'$X|\x91\xe0\xd8'  # base MAC address
mac_robot = {}
for e in robot_mac.items():
    mac_robot[e[1]] = e[0]
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
  addr, msg = e.recv()
  if addr:
#      print('msg:', msg)
      l = msg.split(b'\n')
      if len(l) == 2:
          ville = l[0]
#          print('ville:', ville)
          print("{}:{}".format(mac_robot[addr], ville.decode()))
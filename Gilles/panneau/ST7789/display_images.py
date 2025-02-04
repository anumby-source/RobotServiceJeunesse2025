import os
from machine import Pin, SPI
from st7789py import *
import vga1_16x32 as font
from time import sleep, ticks_ms
import network
import espnow
from gc import collect

robotAddr = b'\x24\x58\x7c\x91\xe3\x60'	# robot mac address
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect() 
e = espnow.ESPNow()
e.active(True)
e.add_peer(robotAddr)

collect()
os.chdir('/ST7789/raw_images')
buf = bytearray(240*80*2)
rotation = 2
tft = ST7789(SPI(1, baudrate=40000000, sck=Pin(4), mosi=Pin(3), miso=None),
                240,
                320,
                reset=Pin(2, Pin.OUT),
                cs=Pin(0, Pin.OUT),
                dc=Pin(1, Pin.OUT),
                rotation=rotation)

while True:
    try:
        for fn in ('stop', 'sens_interdit', 'depassement'):
            t = ticks_ms()
            tft.display_image(fn, buf)
            while ticks_ms() - t < 4000:
                host, msg = e.recv(1)
                if msg:
                    tft.text(font, msg.decode(), 10, 10, RED, background=WHITE)
#                     pass
    except KeyboardInterrupt:
        break

sleep(1)
tft.fill(0)

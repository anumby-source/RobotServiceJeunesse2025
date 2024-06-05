###################################################################
#
#   Test ESP32-cam video streaming via websockets with javascript
#   Works with index.html
#
###################################################################

import os
import socket
import network
from websocket import websocket
import websocket_helper
from time import sleep, sleep_ms
from machine import Pin, Timer, reset
import camera
from neopixel import NeoPixel
from WifiConnect import WifiConnect
from binascii import b2a_base64
#
robot_no = 1
count = 0
#
def cb(tim):
    global count
    count += 1
    buf = b2a_base64(camera.capture())
    ws.write(buf)
#
def notify(s):
    msg = ws.read()

def serve_page(sock):
    try:
        sock.sendall('HTTP/1.1 200 OK\nConnection: close\nServer: WebSocket Server\nContent-Type: text/html\n')
        length = os.stat("tesseract.html")[6]
        sock.sendall('Content-Length: {}\n\n'.format(length))
        # Process page by lines to avoid large strings
        with open("tesseract.html", 'r') as f:
            for line in f:
                sock.sendall(line)
    except OSError:
        print("serve_page : error")
        pass

# camera initialization
camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
# camera.framesize(camera.FRAME_96X96)
# camera.framesize(camera.FRAME_QVGA)   # (320x240)
camera.framesize(camera.FRAME_QQVGA)   # (160x120)
camera.quality(10)
#
#  wifi access point mode
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid="ESP32-cam-{}".format(robot_no), password="")
# # activate server
# s = socket.socket()
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind(('192.168.4.1', 80))
# s.listen(1)
#
#   wifi station mode
sta = WifiConnect('KIWI_11091')
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ai = socket.getaddrinfo("0.0.0.0", 80)
addr = ai[0][4]
s.bind(addr)
s.listen(1)
#
tim = Timer(1)
#
while True:
    try:
        print('listening...')
        cl, remote_addr = s.accept()
        print(remote_addr, ' connected')
        websocket_helper.server_handshake(cl)
        print('ws ok')
        ws = websocket(cl, True)
        cl.setblocking(False)
        cl.setsockopt(socket.SOL_SOCKET, 20, notify)
        tim.init(freq=10, callback=cb)
        while True:
            sleep_ms(10)       
    except OSError:
        serve_page(cl)
    except KeyboardInterrupt:
        cl.setsockopt(socket.SOL_SOCKET, 20, None)
        cl.close()
        break

s.close()
del cl
del s
tim.deinit()
reset()
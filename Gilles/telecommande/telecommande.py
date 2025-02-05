import network
import espnow
from machine import Pin, ADC
from time import sleep_ms
#
def normalize(x):
    x -= midadc
    if x > dzw:
        x = int(100*(x-dzw)/szw)
    elif x < -dzw:
        x = int(100*(x+dzw)/szw)
    else:
        x = 0
    return x
#
def blink():
    for i in range(5):
        led.off()
        sleep_ms(500)
        led.on()
        sleep_ms(500)
#
a0 = ADC(0, atten=ADC.ATTN_11DB)
a1 = ADC(1, atten=ADC.ATTN_11DB)
midadc = 1450         # adc middle
maxadc = 2900         # adc max
dzw    = 200          # dead zone width
szw    = midadc - dzw # sensitive zone width
#
led = Pin(8, Pin.OUT)
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266
#
e = espnow.ESPNow()
e.active(True)
# peer = b'\xe8\x06\x90\x66\x68\x0c'   # display pannel MAC address
peer = b'\x24\x58\x7c\x91\xe3\x60'
e.add_peer(peer)      # Must add_peer() before send()
# 
if e.send("Starting..."):
    blink()
else:
    led.on()
    raise Exception ("Espnow Transmission Error")
#
while True:
    try:
        r, s = a0.read_uv()/1000, a1.read_uv()/1000
        r = normalize(r)     # r in [-100,+100]
        s = normalize(s)     # s in [-100,+100]
        if s < 0 : r = -r
        if s == 0 : r //= 5
        ls = min( max(s+r, -100), 100)
        rs = min( max(s-r, -100), 100)
        cmd = 'ml.set_speed(' + str(ls) + ')\r'
        e.send(cmd.encode())
        cmd = 'mr.set_speed(' + str(rs) + ')\r'
        e.send(cmd.encode())
        sleep_ms(100)
    except:
        led.on()
        break
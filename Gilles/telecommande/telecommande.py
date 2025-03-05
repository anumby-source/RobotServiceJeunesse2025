import network
import espnow
from machine import Pin, ADC
from time import sleep_ms, ticks_ms
#
def normalize(x, amp=100):
    ''' resize x -> [-amp;+amp] '''
    x -= midadc
    if x > dzw:
        x = int(amp*(x-dzw)/szw)
    elif x < -dzw:
        x = int(amp*(x+dzw)/szw)
    else:
        x = 0
    return x
#
def blink():
    ''' blink onboard led '''
    for i in range(5):
        led.off()
        sleep_ms(500)
        led.on()
        sleep_ms(500)
#
def change_mode():
    ''' toggle fast mode <-> slow mode '''
    global samp, ramp
    if samp == 100:
        samp = 30
        ramp = 20
    else:
        samp = 100
        ramp = 50
    print('change mode, samp=', samp)

# init ADC
a0 = ADC(0, atten=ADC.ATTN_11DB)
a1 = ADC(1, atten=ADC.ATTN_11DB)
midadc = 1450         # adc middle
maxadc = 2900         # adc max
dzw    = 200          # dead zone width
szw    = midadc - dzw # sensitive zone width
samp   = 30
ramp   = 20

# init onbard led
led = Pin(8, Pin.OUT)

# init joystick click
p2 = Pin(2, Pin.IN)
pressed = False

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# init espnow
e = espnow.ESPNow()
e.active(True)
print("telecommande.py : Network active, Espnow ok")
# peer = b'\xe8\x06\x90\x66\x68\x0c'   # display pannel MAC address
robot = b'\x24\x58\x7c\x91\xe3\x60'
e.add_peer(robot)      # Must add_peer() before send()
print("telecommande.py : robot added to peers")
#
if e.send("Starting..."):
    blink()
else:
    led.off()
    sleep_ms(2000)
    led.on()
    sleep_ms(2000)
    led.off()
    sleep_ms(2000)
    led.on()
    raise Exception ("Espnow Transmission Error")
#
while True:
    try:
        r, s = a0.read_uv()/1000, a1.read_uv()/1000
        r = normalize(r, ramp)     # r in [-ramp,+ramp]
        s = normalize(s, samp)     # s in [-samp,+samp]
        if s < 0 : r = -r
        if s+r > 100:
            ls, rs = 100, 100-2*r
        elif s+r < -100:
            ls, rs = -100, -100-2*r
        elif s-r > 100:
            ls, rs = 100+2*r, 100
        elif s-r < -100:
            ls, rs = -100+2*r, -100
        else:
            ls, rs = s+r, s-r
        cmd = 'ml.set_speed(' + str(ls) + ')\r'
        cmd += 'mr.set_speed(' + str(rs) + ')\r'
        e.send(cmd.encode())
#         print(cmd.encode())
        sleep_ms(100)
        if (s < samp - 2) and (not p2.value()): # check and debounce click
            if not pressed:
                pressed = True
                change_mode()
                led.value(not led.value())
        else:
            pressed = False
    except:
        led.off()
        break
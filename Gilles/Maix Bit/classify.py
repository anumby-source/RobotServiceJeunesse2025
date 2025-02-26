import KPU as kpu
import sensor
import gc
from fpioa_manager import fm
from Maix import GPIO
from board import board_info
from machine import UART

############### config #################
saved_path = "trafic_v0.classifier"
THRESHOLD = 15
class_names = ['stop', 'sens interdit', 'depass. interdit']
########################################

# initialisation board leds
fm.register(13, fm.fpioa.GPIO0, force=True)     # 13 = board_info.LED_R
fm.register(12, fm.fpioa.GPIOHS0, force=True)   # 12 = board_info.LED_G
fm.register(14, fm.fpioa.GPIO2, force=True)     # 14 = board_info.LED_B
leds = [GPIO(GPIO.GPIO0, GPIO.OUT), GPIO(GPIO.GPIOHS0, GPIO.OUT), GPIO(GPIO.GPIO2, GPIO.OUT)]
for led in leds:
    led.value(255)   # extinction
last_index = -1
# initialisation camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
# initialisation du modele
try:
    del model
except Exception:
    pass
try:
    del classifier
except Exception:
    pass

gc.collect()

model = kpu.load(0x300000)
classifier, class_num, sample_num = kpu.classifier.load(model, saved_path)
# initialisation UART
fm.register(7, fm.fpioa.UART1_TX, force=True)
fm.register(6, fm.fpioa.UART1_RX, force=True)

u = UART(UART.UART1, 115200)

u.write(b'Hello !')
# 
while 1:
    img = sensor.snapshot()
    res_index = -1
    try:
        res_index, min_dist = classifier.predict(img)
    except KeyboardInterrupt:
        break
    if res_index >= 0 and min_dist < THRESHOLD :
        if res_index != last_index:
            leds[last_index].value(1)
            leds[res_index].value(0)
            u.write(str(res_index).encode())
            last_index = res_index
    else:
        if last_index != -1:
            leds[last_index].value(1)
            last_index = -1

for led in leds:
    led.value(255)   # extinction

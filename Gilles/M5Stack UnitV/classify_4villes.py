import KPU as kpu
import sensor
#import lcd
import gc
from modules import ws2812
from machine import UART
from fpioa_manager import fm

############### config #################
saved_path = "4_villes.classifier"
THRESHOLD = 15
class_names = ['paris', 'auxerre', 'lyon', 'marseille']
########################################

# init rgb led
led = ws2812(8,100)
r, v, b, w, blk = (250, 0, 0), (0, 250, 0), (0, 0, 250), (128, 128, 128), (0, 0, 0)
leds = (r, v, b, w)

# init display
#lcd.init()

# init camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))

# init UART
fm.register(34, fm.fpioa.UART1_TX, force=True)
fm.register(35, fm.fpioa.UART1_RX, force=True)
u = UART(UART.UART1, 115200)
u.write(b'Hello !')
u.read(u.any())

# init model
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

pan = None

# process images
while 1:
    img = sensor.snapshot()
    res_index = -1
    try:
        res_index, min_dist = classifier.predict(img)
        #print("{:.2f}".format(min_dist))
    except Exception as e:
        #print("predict err:", e)
       led.set_led(0, blk)
       pan = None
    if res_index >= 0 and min_dist < THRESHOLD :
        #print("predict result:", class_names[res_index])
        if class_names[res_index] != pan:
            pan = class_names[res_index]
            print(pan)
            u.write(pan + '\n')
            led.set_led(0, leds[res_index])
    else:
        #print("unknown, maybe:", class_names[res_index])
        pan = None
        led.set_led(0, blk)

    led.display()
    #lcd.display(img)

import KPU as kpu
import sensor
import lcd
import gc
#from modules import ws2812

############### config #################
saved_path = "3_panneaux.classifier"
THRESHOLD = 18
class_names = ['stop', 'sens-interdit', 'dep-interdit']
########################################

# init rgb led
#led = ws2812(8,100)
#r, v, b, blk = (250, 0, 0), (0, 250, 0), (0, 0, 250), (0, 0, 0)
#leds = (r, v, b)
# init camera
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
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

# process images
while 1:
    img = sensor.snapshot()
    res_index = -1
    try:
        res_index, min_dist = classifier.predict(img)
        print("{:.2f}".format(min_dist))
    except Exception as e:
        print("predict err:", e)
#        led.set_led(0, blk)
    if res_index >= 0 and min_dist < THRESHOLD :
        print("predict result:", class_names[res_index])
#        led.set_led(0, leds[res_index])
    else:
        print("unknown, maybe:", class_names[res_index])
#        led.set_led(0, blk)

#    led.display()
    lcd.display(img)

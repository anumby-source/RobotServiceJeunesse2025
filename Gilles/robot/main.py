# Put your code here

#################################
def start_robot(e):
    Pin(9, Pin.IN).irq(handler=None, trigger=Pin.IRQ_FALLING)
    import robot
        
from machine import Pin
irq = Pin(9, Pin.IN).irq(handler=start_robot, trigger=Pin.IRQ_FALLING)
#################################
# mac = b'$X|\x91\xe3`'   # this device

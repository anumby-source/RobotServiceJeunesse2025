# Put your code here
#################################
def start_robot(e):
    import robot

from machine import Pin
irq = Pin(9, Pin.IN).irq(handler=start_robot, trigger=Pin.IRQ_FALLING)
Pin(6, Pin.OUT).value(0)    # stop left motor
#################################
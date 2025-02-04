# Put your code here
#################################
def start_joystick(e):
    import telecommande

from machine import Pin
irq = Pin(9, Pin.IN).irq(handler=start_joystick, trigger=Pin.IRQ_FALLING)
#################################



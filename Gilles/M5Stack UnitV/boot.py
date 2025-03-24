from fpioa_manager import fm
from Maix import GPIO

# init A & B button
fm.register(18, fm.fpioa.GPIOHS0)
buta = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)
fm.register(19, fm.fpioa.GPIOHS1)
butb = GPIO(GPIO.GPIOHS1, GPIO.IN, GPIO.PULL_UP)

def irq(e):
    buta.irq(None)
    butb.irq(None)
    if e == buta:
        import classify_4villes
    elif e == butb:
        import classify_3panneaux

buta.irq(irq,GPIO.IRQ_BOTH)
butb.irq(irq,GPIO.IRQ_BOTH)

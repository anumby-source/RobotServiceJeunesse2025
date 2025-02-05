# import classify
from fpioa_manager import fm
from Maix import GPIO
from board import board_info

# initialisation bouton BOOT
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
key = GPIO(GPIO.GPIOHS0, GPIO.PULL_UP)

def isr(e):
    key.disirq()
    import classify

key.irq(trigger=key.IRQ_FALLING, handler=isr)
import machine
import utime
from machine import Pin, I2C, Timer
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Constants
I2C_ADDR = 0x20
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
# Prijzen constants
PRIJS_PIEWS = 2  # pin 0
PRIJS_GUST = 3.5 # pin 1 
PRIJS_COCA = 2.5 # pin 2

# LCD setup
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Button pins setup
button_pins_tikken =   [Pin(13, Pin.IN, Pin.PULL_DOWN),    # [0] - piews
                Pin(14, Pin.IN, Pin.PULL_DOWN),     # [1] - gust
                Pin(15, Pin.IN, Pin.PULL_DOWN),     # [2] - coca
                Pin(16, Pin.IN, Pin.PULL_DOWN)]     # [3] - reset
button_pin_BEF = Pin(17, Pin.IN, Pin.PULL_DOWN)

# Global variable(s)
totaal = 0

def print_totaal():
    """Update the total value on the LCD."""
    if totaal < 10:
        lcd.move_to(12, 0)
    elif totaal < 100:
        lcd.move_to(11,0)
    else:
        lcd.move_to(10,0)
    lcd.putstr("{:.2f}".format(totaal)) 
switch_state = 0

def reset():
    lcd.clear()
    UI()

def handler_buttons(pin):
    global totaal,switch_state, PRIJS_PIEWS, PRIJS_COCA, PRIJS_GUST

    if pin == button_pins_tikken[0] and button_pins_tikken[0].value() == 1 and switch_state == 0:
        switch_state = 1
        totaal += PRIJS_PIEWS
    elif pin == button_pins_tikken[1] and button_pins_tikken[1].value() == 1 and switch_state == 0:
        switch_state = 1
        totaal += PRIJS_GUST
    elif pin == button_pins_tikken[2] and button_pins_tikken[2].value() == 1 and switch_state == 0:
        switch_state = 1
        totaal += PRIJS_COCA
    elif pin == button_pins_tikken[3] and button_pins_tikken[3].value() == 1 and switch_state == 0:
        switch_state = 1
        reset()
    else:
        switch_state = 0

    print_totaal()

def handler_to_BEF(pin):
    global totaal
    totaal *= 40
    print_totaal()
    

def welkom():
    for btn in button_pins_tikken:
        btn.irq(handler=None)
    """Display a welcome message on the LCD."""
    lcd.clear()
    lcd.putstr("Jow zadde")
    lcd.move_to(4, 1)
    lcd.putstr("fluidde")
    utime.sleep(2)
    lcd.clear()
def UI():
    """Initialize the user interface on the LCD."""
    global totaal
    totaal = 0
    lcd.move_to(3, 0)
    lcd.putstr("Totaal: ")
    print_totaal()
    lcd.move_to(0, 1)
    lcd.putstr("Piews")
    lcd.move_to(6, 1)
    lcd.putstr("Gust")
    lcd.move_to(11, 1)
    lcd.putstr("Coca")
    for btn in button_pins_tikken:
        btn.irq(handler=handler_buttons)

#setup interrupt request handling
for btn in button_pins_tikken:
    btn.irq(trigger=Pin.IRQ_RISING, handler=handler_buttons)

button_pin_BEF.irq(trigger=Pin.IRQ_RISING, handler=handler_to_BEF)


# Initialize the LCD with welcome message and UI
welkom()
UI()
# Program loop
while True:
    utime.sleep(.0001)
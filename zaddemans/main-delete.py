import machine
import utime
from machine import Pin, I2C, Timer
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import _thread

# Constants
I2C_ADDR = 0x20
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# LCD setup
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Button pins setup
buttons_add =   [Pin(18, Pin.IN, Pin.PULL_DOWN),            # [0] - piews
                Pin(17, Pin.IN, Pin.PULL_DOWN),             # [1] - gust
                Pin(16, Pin.IN, Pin.PULL_DOWN),             # [2] - coca
                Pin(13, Pin.IN, Pin.PULL_DOWN),             # [3] - sparta/H2O
                Pin(14, Pin.IN, Pin.PULL_DOWN),             # [4] - duvel
                Pin(15, Pin.IN, Pin.PULL_DOWN),]            # [5] - wijn/Limonade


button_reset = Pin(10, Pin.IN, Pin.PULL_DOWN)              

button_BEF = Pin(19, Pin.IN, Pin.PULL_DOWN)

# Global variable(s)
total_EUR = 0.0
total_BEF = 0.0

debounce_delay = 70

is_BEF = False

prices_EUR =  [2.5, 
               3.5, 
               2.5,
               2.0,
               4.0,
               4.5]

prices_BEF =  [100,
               140,
               100,
               80,
               160,
               180]

def print_total():
    global is_BEF, total_BEF, total_EUR

    start_time = utime.ticks_ms() #Time recording start

    # Clear the area where the total is displayed
    for i in range(9, 16):
        lcd.move_to(i, 0)
        lcd.putchar(' ')

    # Determine which total to display and its position
    totaal = total_BEF if is_BEF else total_EUR
    formatted_totaal = "{:.0f}".format(totaal) if is_BEF else "{:.2f}".format(totaal)
    
    if totaal < 10:
        position = 14 if is_BEF else 12
    elif totaal < 100:
        position = 13 if is_BEF else 11
    elif totaal < 1000:
        position = 12 if is_BEF else 10
    else:
        position = 11 if is_BEF else 9
    
    lcd.move_to(position, 0)
    lcd.putstr(formatted_totaal)

    end_time = utime.ticks_ms() #Time recording end
    execution_time = utime.ticks_diff(end_time, start_time)  # Calculate the difference
    print("Execution time: {} miliseconds".format(execution_time))

def reset():
    lcd.clear()
    UI()

def handler_buttons(pin):
    global total_EUR, total_BEF, prices_EUR, prices_BEF

    utime.sleep_ms(debounce_delay)

    switch_state_price = False
    print(switch_state_price)

    if pin == buttons_add[0] and buttons_add[0].value() == 1 and switch_state_price == False:   #piews
        switch_state_price = True
        total_EUR += prices_EUR[0]
        total_BEF += prices_BEF[0]
        print(switch_state_price)
        print(total_EUR)
        print(buttons_add[0].value())
    elif pin == buttons_add[1] and buttons_add[1].value() == 1 and switch_state_price == False: #gust
        switch_state_price = True
        total_EUR += prices_EUR[1]
        total_BEF += prices_BEF[1]
    elif pin == buttons_add[2] and buttons_add[2].value() == 1 and switch_state_price == False: #coca
        switch_state_price = True
        total_EUR += prices_EUR[2]
        total_BEF += prices_BEF[2]
    elif pin == buttons_add[3] and buttons_add[3].value() == 1 and switch_state_price == False: #sparta/H2O
        switch_state_price = True
        total_EUR += prices_EUR[3]
        total_BEF += prices_BEF[3]
    elif pin == buttons_add[4] and buttons_add[4].value() == 1 and switch_state_price == False: #duvel
        switch_state_price = True
        total_EUR += prices_EUR[4]
        total_BEF += prices_BEF[4]
    elif pin == buttons_add[5] and buttons_add[5].value() == 1 and switch_state_price == False: #wijn/limonade
        switch_state_price = True
        total_EUR += prices_EUR[5]
        total_BEF += prices_BEF[5]
    
    print_total()

# reset screen
def handler_reset(pin):
    switch_state_reset = False

    if pin == button_reset and button_reset.value() == 1 and switch_state_reset == False: #reset
        switch_state_reset = True
        reset()

# set to BEF or EUR
def handler_to_BEF(pin):
    global is_BEF

    utime.sleep_ms(debounce_delay)

    switch_state_BEF = False

    print(switch_state_BEF)
    if button_BEF.value() == 1 and switch_state_BEF == False:
        switch_state_BEF = True
        is_BEF = not is_BEF
        print(switch_state_BEF)
    print_total()
    

#setup interrupt request handling
def setup_interrupts_pricebtn():
    for btn in buttons_add:
        btn.irq(trigger=Pin.IRQ_RISING, handler=handler_buttons)

button_reset.irq(trigger=Pin.IRQ_RISING, handler=handler_reset)

button_BEF.irq(trigger=Pin.IRQ_RISING, handler=handler_to_BEF)

def welcome():
    # buttons op non-actief zetten
    for btn in buttons_add:
        btn.irq(handler=None)

    # begroeting
    lcd.clear()
    lcd.putstr("Jow zadde")
    lcd.move_to(4, 1)
    lcd.putstr("fluidde")
    utime.sleep(2)
    lcd.clear()
def UI():
    global total_EUR, total_BEF
    
    total_EUR = 0
    total_BEF = 0
    lcd.move_to(2, 0)
    lcd.putstr("Totaal: ")
    print_total()
    lcd.move_to(0, 1)
    lcd.putstr("Piews")
    lcd.move_to(6, 1)
    lcd.putstr("Gust")
    lcd.move_to(11, 1)
    lcd.putstr("Coca")
    setup_interrupts_pricebtn()



# Initialize the LCD with welcome message and UI
welcome()
UI()
# Program loop
while True:
    utime.sleep(.0001)
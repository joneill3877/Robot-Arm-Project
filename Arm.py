import time
import board
from digitalio import DigitalInOut, Direction, Pull
import analogio 
from lcd import LCD
import busio
from i2c_pcf8574_interface import I2CPCF8574Interface
import adafruit_74hc595
from adafruit_motor import stepper
import asyncio

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
latch_pin = DigitalInOut(board.D0)
sr = adafruit_74hc595.ShiftRegister74HC595(spi, latch_pin)
pins = [sr.get_pin(n) for n in range(8)]
btn = DigitalInOut(board.D11)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
ax = analogio.AnalogIn(board.A0)
ay = analogio.AnalogIn(board.A1)
pot_min = 0.00
pot_max = 3.29
step = (pot_max - pot_min) / 20.0
analog_direction = ""
state = 0
i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)
last_position = 0
position = 1
DELAY = 0.01  
STEPS = 100
coilsM1 = (
    digitalio.DigitalInOut(board.D9),   # A1
    digitalio.DigitalInOut(board.D10),  # A2
    digitalio.DigitalInOut(board.D11),  # B1
    digitalio.DigitalInOut(board.D12),  # B2
)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536


def steps(axis):
    return round((axis - pot_min) / step)

while True:
    lcd.clear()
    x = steps(get_voltage(ax))
    y = steps(get_voltage(ay))
    if (x == 10 and y == 10):
        analog_direction = "null"
    if (x == 10 and y == 0):
        analog_direction = "N"
    if (x == 20 and y == 10):
        analog_direction = "E"
    if (x == 0 and y == 10):
        analog_direction = "W"
    if (x == 10 and y == 20):
        analog_direction = "S"
    if (x == 20 and y == 0):
        analog_direction = "NE"
    if (x == 0 and y == 0):
        analog_direction = "NW"
    if (x == 0 and y == 20):
        analog_direction = "SW"
    if (x == 20 and y == 20):
        analog_direction = "SE"
    if btn.value == False:
        lcd.set_cursor_pos(1, 0)
        lcd.print("BTN is down")
        state = 1    
    lcd.set_cursor_pos(0, 0)
    lcd.print(analog_direction)
    time.sleep(.1)

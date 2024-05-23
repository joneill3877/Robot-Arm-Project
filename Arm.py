import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from lcd import LCD
from i2c_pcf8574_interface import I2CPCF8574Interface

ax = AnalogIn(board.A13)
ay = AnalogIn(board.A12)
btn = DigitalInOut(board.A11)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
state = 0
i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)
last_position = 0
position = 1
joystick_direction = "none"

def analog_direction:
  x = map_range(ax, 0, 65535, -1, 1)
  y = map_range(ay, 0, 65535, -1, 1)
  if x >= 0 and y 
while True:


  if not btn.value:
    print("BTN is down")
    state = 1
  time.sleep(0.1) 


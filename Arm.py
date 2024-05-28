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
mode = "menu"
coils = (
    digitalio.DigitalInOut(board.D9),   # A1
    digitalio.DigitalInOut(board.D10),  # A2
    digitalio.DigitalInOut(board.D11),  # B1
    digitalio.DigitalInOut(board.D12),  # B2
    digitalio.DigitalInOut(board.D9),   # A1
    digitalio.DigitalInOut(board.D10),  # A2
    digitalio.DigitalInOut(board.D11),  # B1
    digitalio.DigitalInOut(board.D12),  # B2
    digitalio.DigitalInOut(board.D9),   # A1
    digitalio.DigitalInOut(board.D10),  # A2
    digitalio.DigitalInOut(board.D11),  # B1
    digitalio.DigitalInOut(board.D12),  # B2
)

for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT
motorM1 = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)
motorM2 = stepper.StepperMotor(coils[4], coils[5], coils[6], coils[7], microsteps=None)
motorM3 = stepper.StepperMotor(coils[8], coils[9], coils[10], coils[11], microsteps=None)
motorM4 = stepper.StepperMotor(pins[0], pins[1], pins[2], pins[3], microsteps=None)
motorM5 = stepper.StepperMotor(pins[4], pins[5], pins[6], pins[7], microsteps=None)
armX = 0
armY = 0
clawRot = 0
clawOpen = 0

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def steps(axis):
    return round((axis - pot_min) / step)

def menu():
    if analog_direction == "E":
        if position < 4:
            position += 1
        if position >= 4:
            position = 0
        if position <= 0:
            position = 3
    if analog_direction == "W":
        if position < 4:
            position -= 1
        if position >= 4:
            position = 0
        if position <= 0:
            position = 3     
    if position == 0:
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Menu")
        lcd.set_cursor_pos(1, 0)
        lcd.print("Move Arm")
    elif position == 1:
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Menu")
        lcd.set_cursor_pos(1, 0)
        lcd.print("Move Claw")
    elif position == 2:
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Menu")
        lcd.set_cursor_pos(1, 0)
        lcd.print("Reset")
    elif position == 3:
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Menu")
        lcd.set_cursor_pos(1, 0)
        lcd.print("Calibrate")
    if state == 1:
        if position == 0:
            mode = "arm"
        elif position == 1:
            mode = "claw"
        elif position == 2:
            mode = "reset"
        elif position == 3:
            mode = "calibrate"

    
def run_move_arm():
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("Move Arm")
    lcd.set_cursor_pos(1, 0)
    if analog_direction == "N":
        # M1 +
        # M2 -
        arm_dirY = "+Y"
    if analog_direction == "S":
        # M1 -
        # M2 +
        arm_dirY = "-Y"
    if analog_direction == "E":
        # M3 +
        arm_dirX = "+X"
    if analog_direction == "W":
        # M3 -
        arm_dirX = "-X"
    if analog_direction == "NE":
        # M1 -
        # M2 +
        # M3 +
        arm_dirX = "+X"
        arm_dirY = "+Y"
    if analog_direction == "NW":
        # M1 -
        # M2 +
        # M3 -
        arm_dirX = "-X"
        arm_dirY = "+Y"
    if analog_direction == "SE":
        # M1 +
        # M2 -
        # M3 +
        arm_dirX = "+X"
        arm_dirY = "-Y"
    if analog_direction == "SW":
        # M1 +
        # M2 -
        # M3 -
        arm_dirX = "-X"
        arm_dirY = "-Y"
    if state == 1:
        mode = "claw"
    lcd.print(arm_dirX and ", " and arm_dirY)
    
def run_move_claw():
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("Move Claw")
    lcd.set_cursor_pos(1, 0)
    if analog_direction == "N":
        # M1 +
        # M2 -
        claw_rot = "+"
    if analog_direction == "S":
        # M1 -
        # M2 +
        claw_rot = "-"
    if analog_direction == "E":
        # M3 +
        claw_open = "+"
    if analog_direction == "W":
        # M3 -
        claw_open = "-"
    if analog_direction == "NE":
        # M1 -
        # M2 +
        # M3 +
        claw_rot = "+"
        claw_open = "+"
    if analog_direction == "NW":
        # M1 -
        # M2 +
        # M3 -
        claw_rot = "-"
        claw_open = "+"
    if analog_direction == "SE":
        # M1 +
        # M2 -
        # M3 +
        claw_rot = "+"
        claw_open = "-"
    if analog_direction == "SW":
        # M1 +
        # M2 -
        # M3 -
        claw_rot = "-"
        claw_open = "-"
    if state == 1:
        mode = "arm"
    lcd.print(claw_rot and ", " and claw_open)

def run_reset():
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("Reset")

def run_calibrate):
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("Calibrate")

while True:
    lcd.clear()
    state = 0
    x = steps(get_voltage(ax))
    y = steps(get_voltage(ay))
    if x == 10 and y == 10:
        analog_direction = "null"
    if x == 10 and y == 0:
        analog_direction = "N"
    if x == 20 and y == 10:
        analog_direction = "E"
    if x == 0 and y == 10:
        analog_direction = "W"
    if x == 10 and y == 20:
        analog_direction = "S"
    if x == 20 and y == 0:
        analog_direction = "NE"
    if x == 0 and y == 0:
        analog_direction = "NW"
    if x == 0 and y == 20:
        analog_direction = "SW"
    if x == 20 and y == 20:
        analog_direction = "SE"
    if btn.value == False:
        state = 1
    if mode == "menu":
        menu()
    if mode == "arm":
        run_move_arm()
    if mode == "claw":
        run_move_claw()
    if mode == "reset":
        run_reset()
    if mode == "calibrate":
        run_calibrate()
    time.sleep(.1)

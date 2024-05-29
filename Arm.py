import time
import board
from digitalio import DigitalInOut, Direction, Pull
import analogio 
from lcd import LCD
import busio
from i2c_pcf8574_interface import I2CPCF8574Interface
import adafruit_74hc595
from adafruit_motor import stepper


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
state = 0
i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)
last_position = 0
DELAY = 0.01  
STEPS = 50
mode = "menu"

coils = (
    DigitalInOut(board.D6),   # A1
    DigitalInOut(board.D5),  # A2
    DigitalInOut(board.D3),  # B1
    DigitalInOut(board.D4),  # B2
    DigitalInOut(board.D10),   # A1
    DigitalInOut(board.D9),  # A2
    DigitalInOut(board.D7),  # B1
    DigitalInOut(board.D8),  # B2
    DigitalInOut(board.D13),   # A1
    DigitalInOut(board.D12),  # A2
    DigitalInOut(board.D1),  # B1
    DigitalInOut(board.D2),  # B2
)

for coil in coils:
    coil.direction = Direction.OUTPUT
motorM1 = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)
motorM2 = stepper.StepperMotor(coils[4], coils[5], coils[6], coils[7], microsteps=None)
motorM3 = stepper.StepperMotor(coils[8], coils[9], coils[10], coils[11], microsteps=None)
motorM4 = stepper.StepperMotor(pins[0], pins[1], pins[2], pins[3], microsteps=None)
motorM5 = stepper.StepperMotor(pins[4], pins[5], pins[6], pins[7], microsteps=None)
armX = 0
armY = 0
clawRot = 0
clawOpen = 0
menu_pos = 0
arm_dirX = ""
arm_dirY = ""

def analog_direction():
    if x == 10 and y == 10:
        Adir = "null"
    if x == 10 and y == 0:
        Adir = "N"
    if x == 20 and y == 10:
        Adir = "E"
    if x == 0 and y == 10:
        Adir = "W"
    if x == 10 and y == 20:
        Adir = "S"
    if x == 20 and y == 0:
        Adir = "NE"
    if x == 0 and y == 0:
        Adir = "NW"
    if x == 0 and y == 20:
        Adir = "SW"
    if x == 20 and y == 20:
        Adir = "SE"
    return Adir

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def steps(axis):
    return round((axis - pot_min) / step)

def run_reset():
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("Reset")

def run_calibrate():
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("Calibrate")

while True:
    lcd.clear()
    x = steps(get_voltage(ax))
    y = steps(get_voltage(ay))
    if mode == "menu":
        if analog_direction() == "E":
            if menu_pos < 4:
                menu_pos += 1
            if menu_pos >= 4:
                menu_pos = 0
            if menu_pos < 0:
                menu_pos = 3
        if analog_direction() == "W":
            if menu_pos < 4:
                menu_pos -= 1
            if menu_pos >= 4:
                menu_pos = 0
            if menu_pos < 0:
                menu_pos = 3     
        if menu_pos == 0:
            lcd.clear()
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Move Arm")
        elif menu_pos == 1:
            lcd.clear()
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Move Claw")
        elif menu_pos == 2:
            lcd.clear()
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Reset")
        elif menu_pos == 3:
            lcd.clear()
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Calibrate")
        if state == 1 and mode == "menu":
            if menu_pos == 0:
                mode = "arm"
            elif menu_pos == 1:
                mode = "claw"
            elif menu_pos == 2:
                mode = "reset"
            elif menu_pos == 3:
                mode = "calibrate"
            state = 0
    if mode == "arm":
        arm_dirX = ""
        arm_dirY = ""
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Move Arm")
        lcd.set_cursor_pos(1, 0)
        if analog_direction() == "N":
            motorM1.onestep(direction=stepper.BACKWARD)
            arm_dirY = "+Y"
            time.sleep(.01)
            print("moved up")
        if analog_direction() == "S":
            motorM2.onestep(style=stepper.DOUBLE)
            motorM1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            arm_dirY = "-Y"
            time.sleep(.01)
        while analog_direction() == "E":
            # M3 +
            arm_dirX = "+X"
        if analog_direction() == "W":
            # M3 -
            arm_dirX = "-X"
        if analog_direction() == "NE":
            # M1 -
            # M2 +
            # M3 +
            arm_dirX = "+X"
            arm_dirY = "+Y"
        if analog_direction() == "NW":
            # M1 -
            # M2 +
            # M3 -
            arm_dirX = "-X"
            arm_dirY = "+Y"
        if analog_direction() == "SE":
            # M1 +
            # M2 -
            # M3 +
            arm_dirX = "+X"
            arm_dirY = "-Y"
        if analog_direction() == "SW":
            # M1 +
            # M2 -
            # M3 -
            arm_dirX = "-X"
            arm_dirY = "-Y"
        lcd.print(arm_dirX + ", " + arm_dirY)
        if state == 1:
            mode = "menu"
            state = 0
    if mode == "claw":
        claw_rot = ""
        claw_open = ""
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Move Claw")
        lcd.set_cursor_pos(1, 0)
        if analog_direction() == "N":
            # M4 -
            claw_rot = "+"
        if analog_direction() == "S":
            # M4 +
            claw_rot = "-"
        if analog_direction() == "E":
            # M5 +
            claw_open = "+"
        if analog_direction() == "W":
            # M5 -
            claw_open = "-"
        if analog_direction() == "NE":
            # M4 -
            # M5 +
            claw_rot = "+"
            claw_open = "+"
        if analog_direction() == "NW":
            # M4 -
            # M5 -
            claw_rot = "-"
            claw_open = "+"
        if analog_direction() == "SE":
            # M4 +
            # M5 +
            claw_rot = "+"
            claw_open = "-"
        if analog_direction() == "SW":
            # M4 +
            # M5 -
            claw_rot = "-"
            claw_open = "-"
        lcd.print(claw_rot + ", " + claw_open)
        if state == 1:
            mode = "menu"
            state = 0
    if mode == "reset":
        run_reset()
    if mode == "calibrate":
        run_calibrate()
    
    if btn.value == False:
        state = 1
    elif btn.value == True:
        state = 0    
    time.sleep(.1)

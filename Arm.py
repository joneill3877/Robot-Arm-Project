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
recordPress = 0
switchState = 0
recording = []
recordingNow = False
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
aDir = "null"
rbtn = DigitalInOut(board.A4)
rbtn.direction = Direction.INPUT
rbtn.pull = Pull.UP
mbtn = DigitalInOut(board.A5)
mbtn.direction = Direction.INPUT
mbtn.pull = Pull.UP
def analog_direction():
    if x <= 11 and x >= 9 and y <= 11 and y >= 9:
        return str("null")
    elif x >= 9 and x <= 11 and y >= 0 and y <=2:
        return str("N")
    elif x == 20 and y >= 9 and y <=11:
        return str("E")
    elif x >= 0 and x <= 2 and y >= 9 and y <= 11:
        return str("W")
    elif x >= 9 and x <= 11 and y == 20:
        return str("S")
    elif x == 20 and y >= 0 and y <= 2:
        return str("NE")
    elif x == 0 and y == 0:
        return str("NW")
    elif x <= 3 and y == 20:
        return str("SW")
    elif x == 20 and y == 20:
        return str("SE")

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def steps(axis):
    return round((axis - pot_min) / step)


while True:
    x = steps(get_voltage(ax))
    y = steps(get_voltage(ay))
    print(x, y)
    if mode == "menu":
        lcd.clear()
        if analog_direction() == "E":
            if menu_pos < 5:
                menu_pos += 1
            if menu_pos >= 5:
                menu_pos = 0
            if menu_pos < 0:
                menu_pos = 4
        if analog_direction() == "W":
            if menu_pos < 5:
                menu_pos -= 1
            if menu_pos >= 5:
                menu_pos = 0
            if menu_pos < 0:
                menu_pos = 4     
        if menu_pos == 0:
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Move Arm")
        elif menu_pos == 1:
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Move Claw")
        elif menu_pos == 2:
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Reset")
        elif menu_pos == 3:
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Calibrate")
        elif menu_pos == 4:
            lcd.set_cursor_pos(0, 0)
            lcd.print("Menu")
            lcd.set_cursor_pos(1, 0)
            lcd.print("Play")
        if state == 1 and mode == "menu":
            if menu_pos == 0:
                mode = "arm"
            elif menu_pos == 1:
                mode = "claw"
            elif menu_pos == 2:
                mode = "reset"
            elif menu_pos == 3:
                mode = "calibrate"
            elif menu_pos == 4:
                mode = "play"
            state = 0
        time.sleep(.1)
    if mode == "arm":
        aDir = analog_direction()
        arm_dirX = ""
        arm_dirY = ""
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Move Arm")
        lcd.set_cursor_pos(1, 0)
        if analog_direction() == "N":
            motorM2.onestep(style=stepper.DOUBLE)
            motorM1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            arm_dirY = "+Y"
            if recordingNow == True:
                recording.append("AN")
        if analog_direction() == "S":
            motorM1.onestep(style=stepper.DOUBLE)
            motorM2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            arm_dirY = "-Y"
            if recordingNow == True:
                recording.append("AS")
        if analog_direction() == "E":
            motorM3.onestep(style=stepper.DOUBLE)
            arm_dirX = "+X"
            if recordingNow == True:
                recording.append("AE")   
        if analog_direction() == "W":
            motorM3.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            arm_dirX = "-X"
            if recordingNow == True:
                recording.append("AW")
        if analog_direction() == "NE":
            motorM2.onestep(style=stepper.DOUBLE)
            motorM1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            motorM3.onestep(style=stepper.DOUBLE)
            arm_dirX = "+X"
            arm_dirY = "+Y"
            if recordingNow == True:
                recording.append("ANE")
        if analog_direction() == "NW":
            motorM1.onestep(style=stepper.DOUBLE)
            motorM2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            motorM3.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            arm_dirX = "-X"
            arm_dirY = "+Y"
            if recordingNow == True:
                recording.append("ANW")
        if analog_direction() == "SE":
            motorM1.onestep(style=stepper.DOUBLE)
            motorM2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            motorM3.onestep(style=stepper.DOUBLE)
            arm_dirX = "+X"
            arm_dirY = "-Y"
            if recordingNow == True:
                recording.append("ASE")
        if analog_direction() == "SW":
            motorM1.onestep(style=stepper.DOUBLE)
            motorM2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            motorM3.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            arm_dirX = "-X"
            arm_dirY = "-Y"
            if recordingNow == True:
                recording.append("ASW")
        lcd.print(arm_dirX + ", " + arm_dirY)
        if state == 1:
            mode = "menu"
            state = 0
            time.sleep(1)
        if switchState == 1:
            mode = "arm"
            switchState = 0
    if mode == "claw":
        claw_rot = ""
        claw_open = ""
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Move Claw")
        lcd.set_cursor_pos(1, 0)
        if analog_direction() == "N":
            motorM4.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            claw_rot = "+"
            if recordingNow == True:
                recording.append("CN")
        if analog_direction() == "S":
            motorM4.onestep(style=stepper.DOUBLE)
            claw_rot = "-"
            if recordingNow == True:
                recording.append("CS")
        if analog_direction() == "E":
            motorM5.onestep(style=stepper.DOUBLE)
            claw_open = "+"
            if recordingNow == True:
                recording.append("CE")
        if analog_direction() == "W":
            motorM5.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            claw_open = "-"
            if recordingNow == True:
                recording.append("CW")
        if analog_direction() == "NE":
            motorM4.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            motorM5.onestep(style=stepper.DOUBLE)
            claw_rot = "+"
            claw_open = "+"
            if recordingNow == True:
                recording.append("CNE")
        if analog_direction() == "NW":
            motorM4.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            motorM5.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            claw_rot = "-"
            claw_open = "+"
            if recordingNow == True:
                recording.append("CNW")
        if analog_direction() == "SE":
            motorM4.onestep(style=stepper.DOUBLE)
            motorM5.onestep(style=stepper.DOUBLE)
            claw_rot = "+"
            claw_open = "-"
            if recordingNow == True:
                recording.append("CSE")
        if analog_direction() == "SW":
            motorM4.onestep(style=stepper.DOUBLE)
            motorM5.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            claw_rot = "-"
            claw_open = "-"
            if recordingNow == True:
                recording.append("CSW")
        lcd.print(claw_rot + ", " + claw_open)
        if state == 1:
            mode = "menu"
            state = 0
        if switchState == 1:
            mode = "claw"
            switchState = 0
    if mode == "reset":
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Reset")
    if mode == "calibrate":
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Calibrate")
    if mode == "play":
        lcd.clear()
        lcd.set_cursor_pos(0, 0)
        lcd.print("Play")
    if btn.value == False:
        switchState = 1
    elif btn.value == True:
        switchState = 0
    if rbtn.value == False:
        recordPress = 1
    elif rbtn.value == True:
        recordPress = 0
    if mbtn.value == False:
        state = 1
    elif mbtn.value == True:
        state = 0
    

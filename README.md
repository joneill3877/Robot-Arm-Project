# 23/24 Engeering 4 Robot Arm Project 
## Programmable Multi-Axis Robot Arm
By Luke Wylie and Joshua O'Neill Rossouw

## Table of Contents
1. [Planning](#planning)
   1. [Scope](#scope)
   2. [Schedule](#schedule)
   3. [Diagrams](#diagrams)
   4. [Bill of Materials](#bill-of-materials)
   5. [Pseudocode](#pseudocode)
2. [Documentation](#documentation)
   1. [CAD](#cad)
   2. [Code](#code)
   3. [Wiring Diagram](#wiring-diagram)
   4. [Evidence](#evidence)
   5. [Reflective Schedule](#reflective-schedule)
   6. [Reflection](#reflection)

# Planning
## Scope
In this project, we will create a programmable robot arm that can record and loop user inputs to repeat the movements necessary to complete a specific task. The base will be able to clamp onto a surface to stabilize the arm and provide an axis of rotation for the arm. The arm will be constructed out of three hinge joints one connecting the arm base to the first arm segment, the second between the first and second arm segments, and the third between the second arm joint and the claw assembly. The claw comprises four individual blades centered around a central worm gear, which is actuated by a motor, which rotates the blades. A user input device, tethered by a heat-shrunk length of wires, will send inputs to the arm. The inputs on the control device will be a joystick for the axial movements of the joints, a button that switches the joystick to controlling the claw when pressed once and switches back to controlling the arm when pressed again, a button that starts and stops the recording of the inputs, and a button which accesses the menu on the readout LCD. The readout LCD will also be located on the control device and will display pertinent information regarding the movement of the arm.

## Schedule
| Week                        |  Goal                                                                                     |
| :-------------------------: |  :-------------------------------------------------------------------------------------:  |
| Week 1 (March 25-29) |  Finish planning document and CAD for the arm.  |
| Week 2 (April 8-12)  |  Print the arm and start designing the controller.  |
| Week 3 (April 15-19) |  Finish and print the controller.  |
| Week 4 (April 22-26) |  Start assembling the arm and coding the arm control input.  |
| Week 5 (April 29-May 3) |  Start assembling the controller and coding the record functionality.  |
| Week 6 (May 6-10) |  Finish coding and assembling the project.  |
| Week 7 (May 13-17) |  Test the functionality and start the documentation.  |
| Week 8 (May 20-24) |  Finish the documentation.  |

Note: This is a tentative schedule for illustrative purposes, and subject to change based numerous factor such as how the completion of different steps and when the official project due date. 
## Diagrams
<img src="20240325_164954.jpg" alt="Planning Diagram" width="400" height="500">

## Bill Of Materials
|  Name  |  Description  |  Quantity  |
| :----: | :-----------: | :--------: |
| Nema 17 | Stepper Motor | 5 |
| Metro M4 Airlift | Microcontroller Board | 1 |

		
		

## Pseudocode

```python
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import neopixel


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(1)

    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
```


# Documentation

## CAD
[Link to onshape](https://cvilleschools.onshape.com/documents/e30ffb94e8ba368b6e045edf/w/2e96059f558c7828030257d8/e/bc3dcf792d39e192dca5e8ad)

## Code

```python
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import neopixel


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(1)

    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
```

## Wiring Diagram

![](https://github.com/SempronChip/engr3/blob/v1/images/134725601-72db0fcb-0d50-486c-aff5-9e0ec1772057.png?raw=true)

## Evidence

https://github.com/SempronChip/engr3/assets/143545309/e74b0bae-ce39-4a23-b4f0-3eb728cfd7ae

Credit goes to 
[Gaby D.](https://github.com/gdaless20/Circuitpython)

## Reflective Schedule
| Week                        |  Goal                                                                                     |
| :-------------------------: |  :-------------------------------------------------------------------------------------:
| Week 1 (March 25-29) |  Finish planning document and CAD for the arm.  |
| Week 2 (April 8-12)  |  Print the arm and start designing the controller.  |
| Week 3 (April 15-19) |  Finish and print the controller.  |
| Week 4 (April 22-26) |  Start assembling the arm and coding the arm control input.  |
| Week 5 (April 29-May 3) |  Start assembling the controller and coding the record functionality.  |
| Week 6 (May 6-10) |  Finish coding and assembling the project.  |
| Week 7 (May 13-17) |  Test the functionality and start the documentation.  |
| Week 8 (May 20-24) |  Finish the documentation.  |

## Reflection


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
In this project, we will create a programmable robot arm to record and loop user inputs to repeat the movements necessary to complete a specific task. The base will be able to clamp onto a surface to stabilize the arm and provide an axis of rotation for the arm. The arm will be constructed out of three hinge joints one connecting the arm base to the first arm segment, the second between the first and second arm segments, and the third between the second arm joint and the claw assembly. The claw comprises four individual blades centered around a central worm gear, which is actuated by a motor, which rotates the blades. A user input device, tethered by a heat-shrunk length of wires, will send inputs to the arm. The inputs on the control device will be a joystick for the axial movements of the joints, a button that switches the joystick to controlling the claw when pressed once and switches back to controlling the arm when pressed again, a button that starts and stops the recording of the inputs, and a button which accesses the menu on the readout LCD. The readout LCD will also be located on the control device and will display pertinent information regarding the movement of the arm.

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

Note: This is a tentative schedule for illustrative purposes, and is subject to change based on numerous factors such as the completion of different steps and when the official project due date. 
## Diagrams
<img src="20240325_164954.jpg" alt="Planning Diagram" width="400" height="500">

## Bill Of Materials
|  Name  |  Description  |  Quantity  |
| :----: | :-----------: | :--------: |
| Nema 17 | Stepper Motor | 5 |
| Metro M4 Airlift | Microcontroller Board | 1 |

		
		

## Pseudocode

```
Setup motors
Setup analog stick
Setup LCD
Define variables
Define states
Define Menus
While the analog stick is moved and in the arm state:
Move the arm motors this way
Print the movement to the LCD
When the analog stick button is pressed:
Change state
Print state change to the LCD
While the analog stick is moved and in the claw state:
Move the claw motors this way
Print the movement to the LCD
When the record button is pressed and the record is OFF:
Change record to ON
Print the record ON to the LCD
While the record is ON:
Save the movements the arm makes and state changes
If the record button is pressed again stop recording
When play is pressed
Play the saved movements
When the menu is opened:
Print to LCD the menu item
When the analog stick is moved on the menu:
Move to the next menu item
When play is pressed on the menu:
Run the menu item's corresponding function
```


# Documentation

## CAD
[Link to onshape](https://cvilleschools.onshape.com/documents/e30ffb94e8ba368b6e045edf/w/2e96059f558c7828030257d8/e/bc3dcf792d39e192dca5e8ad)

## Code

```python

```

## Wiring Diagram



## Evidence



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


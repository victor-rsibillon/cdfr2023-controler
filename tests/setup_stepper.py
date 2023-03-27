import sys
import time

from totormetrix import totormetrix

"""
Attach a pin to a servo and move it about.
"""

# some globals
PULSE_PIN = 2
DIRECTION_PIN = 3

# Create a Telemetrix instance.
board = totorotrix.Telemetrix(arduino_instance_id=2, arduino_wait=2)

currentStep = 0
stepper_running = False


def the_callback(data):
    global stepper_running
    stepper_running = False


def stepper_goto(destination, await_end=False):
    board.stepper_move_to(motor, destination)
    if await_end:
        global stepper_running
        stepper_running = True
        board.stepper_run(motor, completion_callback=the_callback)
        while stepper_running:
            time.sleep(0.1)


motor = board.set_pin_mode_stepper(interface=2, pin1=PULSE_PIN, pin2=DIRECTION_PIN)
# set the max speed and acceleration
board.stepper_set_current_position(0, 0)
speed = 2700
board.stepper_set_max_speed(motor, speed)
board.stepper_set_speed(motor, speed)
board.stepper_set_acceleration(motor, 1000)

stepper_goto(currentStep, True)

print('Calibration start, enter step value you want and -1 if you want to exit')

while True:
    newAngle = int(input('Step ?='))
    if newAngle == -1:
        break
    print(f'Moving from {currentStep}st to {newAngle}st')
    stepper_goto(newAngle, True)
    currentStep = newAngle

print(f'Calibration ended, last step value is {currentStep}st')

time.sleep(.2)
board.shutdown()

import sys
import time

from telemetrix import telemetrix

"""
Attach a pin to a servo and move it about.
"""

# some globals
SERVO_PIN_LEFT = 24  # 90 open, 170 close
SERVO_PIN_RIGHT = 25  # 90 open, 20 close

# Create a Telemetrix instance.
board = telemetrix.Telemetrix(arduino_instance_id=2, arduino_wait=3)

board.set_pin_mode_servo(SERVO_PIN_LEFT)
board.set_pin_mode_servo(SERVO_PIN_RIGHT)

def closeBothArm():
    board.servo_write(SERVO_PIN_LEFT, 180)
    board.servo_write(SERVO_PIN_RIGHT, 10)

def openBothArm():
    board.servo_write(SERVO_PIN_LEFT, 90)
    board.servo_write(SERVO_PIN_RIGHT, 70)

print('Start')

for i in range(4):
    openBothArm()
    time.sleep(1)
    closeBothArm()
    time.sleep(1)

print('End')
# time.sleep(1)

board.servo_detach(SERVO_PIN_LEFT)
board.servo_detach(SERVO_PIN_RIGHT)
time.sleep(.2)
board.shutdown()

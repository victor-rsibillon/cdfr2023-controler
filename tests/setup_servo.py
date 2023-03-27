import sys
import time

from telemetrix import telemetrix

"""
Attach a pin to a servo and move it about.
"""

# some globals
SERVO_PIN = 17

# Create a Telemetrix instance.
board = telemetrix.Telemetrix(arduino_instance_id=2, arduino_wait=2)

board.set_pin_mode_servo(SERVO_PIN)

currentAngle = 90
board.servo_write(SERVO_PIN, currentAngle)

print('Calibration start, enter angle value you want and -1 if you want to exit')

while True:
    newAngle = int(input('Angle ?='))
    if newAngle == -1:
        break
    print(f'Moving from {currentAngle}° to {newAngle}°')
    board.servo_write(SERVO_PIN, newAngle)
    currentAngle = newAngle

print(f'Calibration ended, last angle value is {currentAngle}°')
# time.sleep(1)

board.servo_detach(SERVO_PIN)
time.sleep(.2)
board.shutdown()

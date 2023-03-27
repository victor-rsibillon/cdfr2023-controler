import sys
import time

from telemetrix import telemetrix

"""
Attach a pin to a servo and move it about.
"""

# some globals
BLINK_LED = 13

# Create a Telemetrix instance.
board = telemetrix.Telemetrix(arduino_instance_id=2, arduino_wait=4)
board.set_pin_mode_digital_output(BLINK_LED)
for i in range(20):
    print('1')
    board.digital_write(BLINK_LED, 1)
    time.sleep(0.5)
    print('0')
    board.digital_write(BLINK_LED, 0)
    time.sleep(0.5)

print('End')
time.sleep(.2)
board.shutdown()
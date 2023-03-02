import sys
import time
from telemetrix import telemetrix

"""
This example sets up and control an ADXL345 i2c accelerometer.
It will continuously print data the raw xyz data from the device.
"""


# the call back function to print the adxl345 data
def the_callback(data):
    """
    :param data: [pin_type, Device address, device read register, x data pair, y data pair, z data pair]
    :return:
    """
    print(data)


def adxl345(my_board):
    # setup adxl345
    # device address = 83
    my_board.set_pin_mode_i2c()


    for i in range(4):
        # read 6 bytes from the data register
        try:
            my_board.i2c_read(42, 50, 1, the_callback)
            time.sleep(.1)

        except (KeyboardInterrupt, RuntimeError):
            my_board.shutdown()
            sys.exit(0)


board = telemetrix.Telemetrix()
try:
    adxl345(board)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
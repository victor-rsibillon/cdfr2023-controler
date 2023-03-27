"""
 Copyright (c) 2022 Alan Yorinks All rights reserved.
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.
 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import sys
import time

from totormetrix.totormetrix import Telemetrix

PULSE_PIN = 2
DIRECTION_PIN = 3
SERVO_PIN_LEFT = 16  # 90 open, 170 close
SERVO_PIN_RIGHT = 15  # 90 open, 20 close

# flag to keep track of the number of times the callback
# was called. When == 2, exit program
stepper_running = False
exit_flag = 0

# instantiate telemetrix
board = Telemetrix(arduino_instance_id=2, arduino_wait=2)


def the_callback(data):
    global exit_flag
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[2]))
    global stepper_running
    stepper_running = False
    print(f'Motor {data[1]} absolute motion completed at: {date}.')
    exit_flag += 1


def running_callback(data):
    if data[1]:
        print('The motor is running.')
    else:
        print('The motor IS NOT running.')


def close_both_arms():
    board.servo_write(SERVO_PIN_LEFT, 178)  # Ok
    board.servo_write(SERVO_PIN_RIGHT, 10)  # Ok


def open_both_arms():
    board.servo_write(SERVO_PIN_LEFT, 85)  # Ok
    board.servo_write(SERVO_PIN_RIGHT, 95)  # Ok


def stepper_goto(destination, await_end=False):
    board.stepper_move_to(motor, destination)
    if await_end:
        global stepper_running
        stepper_running = True
        board.stepper_run(motor, completion_callback=the_callback)
        while stepper_running:
            time.sleep(0.1)


try:
    # start the main function
    # create an accelstepper instance for a TB6600 motor drive
    # if you are using a micro stepper controller board:
    # pin1 = pulse pin, pin2 = direction
    motor = board.set_pin_mode_stepper(interface=2, pin1=PULSE_PIN, pin2=DIRECTION_PIN)
    board.set_pin_mode_servo(SERVO_PIN_LEFT)
    board.set_pin_mode_servo(SERVO_PIN_RIGHT)
    close_both_arms()

    # if you are using a 28BYJ-48 Stepper Motor with ULN2003
    # comment out the line above and uncomment out the line below.
    # motor = board.set_pin_mode_stepper(interface=4, pin1=5, pin2=4, pin3=14,
    # pin4=12)

    # board.stepper_is_running(motor, callback=running_callback)
    time.sleep(.5)

    # set the max speed and acceleration
    board.stepper_set_current_position(0, 0)
    speed = 2500
    board.stepper_set_max_speed(motor, speed)
    board.stepper_set_speed(motor, speed)
    board.stepper_set_acceleration(motor, 1000)

    close_both_arms()
    time.sleep(1)

    # set the absolute position in steps
    stepper_goto(-3000, True)

    print('Starting motor... 2/2')
    stepper_goto(0, True)
    open_both_arms()
    time.sleep(1.5)

    board.servo_detach(SERVO_PIN_LEFT)
    board.servo_detach(SERVO_PIN_RIGHT)
    board.shutdown()
    sys.exit(0)
    board.shutdown()
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)

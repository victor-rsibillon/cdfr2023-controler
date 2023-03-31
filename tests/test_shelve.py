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
SERVO_PIN_LEFT = 15  # 90 open, 170 close
SERVO_PIN_RIGHT = 16  # 90 open, 20 close
SERVO_PIN_SHELF_3 = 20
SERVO_PIN_SHELF_2 = 19
SERVO_PIN_SHELF_1 = 18

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


def close_both_arms(await_end=False):
    board.servo_write(SERVO_PIN_LEFT, 178)  # Ok
    board.servo_write(SERVO_PIN_RIGHT, 10)  # Ok
    if await_end:
        time.sleep(0.5)


def open_both_arms(await_end=False):
    board.servo_write(SERVO_PIN_LEFT, 70)  # Ok
    board.servo_write(SERVO_PIN_RIGHT, 110)  # Ok
    if await_end:
        time.sleep(0.5)


def extend_shelf(shelf_id=1, await_end=False):
    if shelf_id == 1:
        board.servo_write(SERVO_PIN_SHELF_1, 5)
    elif shelf_id == 2:
        board.servo_write(SERVO_PIN_SHELF_2, 5)
    elif shelf_id == 3:
        board.servo_write(SERVO_PIN_SHELF_3, 5)
    if await_end:
        time.sleep(2)


def retract_shelf(shelf_id=1, await_end=False):
    if shelf_id == 1:
        board.servo_write(SERVO_PIN_SHELF_1, 170)
    elif shelf_id == 2:
        board.servo_write(SERVO_PIN_SHELF_2, 170)
    elif shelf_id == 3:
        board.servo_write(SERVO_PIN_SHELF_3, 170)
    if await_end:
        time.sleep(2)


def stepper_goto(destination, await_end=False):
    board.stepper_move_to(motor, destination)
    if await_end:
        global stepper_running
        stepper_running = True
        board.stepper_run(motor, completion_callback=the_callback)
        while stepper_running:
            time.sleep(0.1)


def move_full_stack(from_location, to_location):
    # 0 = ground level
    # 1,2,3 = first, second, third shelf
    assert from_location != to_location


try:
    # Stepper setup
    motor = board.set_pin_mode_stepper(interface=2, pin1=PULSE_PIN, pin2=DIRECTION_PIN)
    # set the max speed and acceleration
    board.stepper_set_current_position(0, 0)
    speed = 2700
    board.stepper_set_max_speed(motor, speed)
    board.stepper_set_speed(motor, speed)
    board.stepper_set_acceleration(motor, 2500)

    # Servo setup
    board.set_pin_mode_servo(SERVO_PIN_SHELF_3)
    board.set_pin_mode_servo(SERVO_PIN_SHELF_2)
    board.set_pin_mode_servo(SERVO_PIN_SHELF_1)

    # Strategy
    # close_both_arms(True)
    retract_shelf(3, True)
    retract_shelf(2, True)
    retract_shelf(1, True)
    time.sleep(1)
    extend_shelf(3, True)
    extend_shelf(2, True)
    extend_shelf(1, True)
    time.sleep(1)
    retract_shelf(3, True)
    retract_shelf(2, True)
    retract_shelf(1, True)
    # End

    board.servo_detach(SERVO_PIN_SHELF_3)
    board.servo_detach(SERVO_PIN_SHELF_2)
    board.servo_detach(SERVO_PIN_SHELF_1)
    board.shutdown()
    sys.exit(0)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)

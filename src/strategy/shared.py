from enum import Enum
from driver.controller import Controller
from driver.portctrl import PortsController
import logging
import time

# > Stepper
STEPPER_PULSE_PIN = 2
STEPPER_DIRECTION_PIN = 3
STEPPER_SPEED = 2500
STEPPER_ACCELERATION = 1000

# > Servos
SERVO_PIN_LEFT = 15  # baterry side
SERVO_OPEN_LEFT = 70
SERVO_CLOSE_LEFT = 178

SERVO_PIN_RIGHT = 16  # lattepanda side
SERVO_OPEN_RIGHT = 110
SERVO_CLOSE_RIGHT = 10

SERVO_PIN_SHELF_3 = 20  # top
SERVO_PIN_SHELF_2 = 19  # middle
SERVO_PIN_SHELF_1 = 18  # bottom
SERVO_EXTEND_SHELVE = 5
SERVO_RETRACT_SHELVE = 170

# > I2C (Carte moteur)
MOTORCARD_I2C_ADDRESS = 42

# Cards properties
main_controller = 'ltp3'
ext_controller = 'mega'


def int_to_str16(val: int):
    v = hex((val + (1 << 16)) % (1 << 16))[2:].zfill(4)
    return [v[:2], v[2:]]


def int_to_int16(val: int):
    v = hex((val + (1 << 16)) % (1 << 16))[2:].zfill(4)
    return [int(v[:2], 16), int(v[2:], 16)]


class MotorCommand:
    def __init__(self, name: str, i2c_cmd: int, i2c_response_len: int):
        self.name = name,
        self.i2c_cmd = i2c_cmd
        self.i2c_response_len = i2c_response_len


class MotorCommands(Enum):
    LED1ON = MotorCommand("led_1_on", 10, 0)
    LED1OFF = MotorCommand("led_1_off", 11, 0)
    LED2ON = MotorCommand("led_2_on", 12, 0)
    LED2OFF = MotorCommand("led_2_off", 13, 0)

    GETPOSITION = MotorCommand("get_pos", 20, 6)  # Recieve 6 bytes: (uint16_t) x, (uint16_t) y, (uint16_t) theta
    SETPOSITION = MotorCommand("set_pos", 21, 0)  # Send 6 bytes: (uint16_t) x, (uint16_t) y, (uint16_t) theta

    GOTOLINEAR = MotorCommand("goto_linear", 30, 0)  # Send 6 bytes: (uint16_t) x, (uint16_t) y, (uint16_t) direction
    GOTOANGLE = MotorCommand("goto_angle", 31, 0)  # Send 2 bytes: (uint16_t) teta
    STOPMOTOR = MotorCommand("stop", 32, 0)

    ERRANGULAR = MotorCommand("error_angular", 33, 2)  # Receive 2 bytes: (uint16_t) error
    ERRLINEAR = MotorCommand("error_linear", 34, 2)  # Receive 2 bytes: (uint16_t) error


class Strategy:
    def __init__(self, port_ctrl: PortsController, debug=False):
        self.port_ctrl = port_ctrl
        self.robot_state = None
        self.debug = debug
        self.stepper_running = False
        self.is_waiting_i2c = False
        self.last_i2c_response = []
        self.stepper = None

    def close_both_arms(self, await_end=False):
        self.external_board().get_board().servo_write(SERVO_PIN_LEFT, SERVO_CLOSE_LEFT)
        self.external_board().get_board().servo_write(SERVO_PIN_RIGHT, SERVO_CLOSE_RIGHT)
        if await_end:
            time.sleep(0.5)

    def open_both_arms(self, await_end=False):
        self.external_board().get_board().servo_write(SERVO_PIN_LEFT, SERVO_OPEN_LEFT)
        self.external_board().get_board().servo_write(SERVO_PIN_RIGHT, SERVO_OPEN_RIGHT)
        if await_end:
            time.sleep(0.5)

    def extend_shelf(self, shelf_id=1, await_end=False):
        if shelf_id == 1:
            self.external_board().get_board().servo_write(SERVO_PIN_SHELF_1, SERVO_EXTEND_SHELVE)
        elif shelf_id == 2:
            self.external_board().get_board().servo_write(SERVO_PIN_SHELF_2, SERVO_EXTEND_SHELVE)
        elif shelf_id == 3:
            self.external_board().get_board().servo_write(SERVO_PIN_SHELF_3, SERVO_EXTEND_SHELVE)
        if await_end:
            time.sleep(2)

    def retract_shelf(self, shelf_id=1, await_end=False):
        if shelf_id == 1:
            self.external_board().get_board().servo_write(SERVO_PIN_SHELF_1, SERVO_RETRACT_SHELVE)
        elif shelf_id == 2:
            self.external_board().get_board().servo_write(SERVO_PIN_SHELF_2, SERVO_RETRACT_SHELVE)
        elif shelf_id == 3:
            self.external_board().get_board().servo_write(SERVO_PIN_SHELF_3, SERVO_RETRACT_SHELVE)
        if await_end:
            time.sleep(2)

    def stepper_callback(self, data):
        self.stepper_running = False
        print(f'Motor {data[1]} absolute motion completed')

    def stepper_goto(self, destination, await_end=False):
        self.external_board().get_board().stepper_move_to(self.stepper, destination)
        if await_end:
            self.stepper_running = True
            self.external_board().get_board().stepper_run(self.stepper, completion_callback=self.stepper_callback)
            while self.stepper_running:
                time.sleep(0.1)

    def external_board(self) -> Controller:
        return self.port_ctrl.ctrls[ext_controller]

    def get_robot_state(self) -> dict:
        return self.robot_state

    def setup_std_pins(self, robot_state: dict):
        # -> Shared dict object
        self.robot_state = robot_state

        # -> I2C
        self.external_board().get_board().set_pin_mode_i2c()

        # -> Servo
        self.external_board().get_board().set_pin_mode_servo(SERVO_PIN_SHELF_1)
        self.external_board().get_board().set_pin_mode_servo(SERVO_PIN_SHELF_2)
        self.external_board().get_board().set_pin_mode_servo(SERVO_PIN_SHELF_3)
        self.external_board().get_board().set_pin_mode_servo(SERVO_PIN_LEFT)
        self.external_board().get_board().set_pin_mode_servo(SERVO_PIN_RIGHT)

        # -> Stepper
        self.stepper = self.external_board().get_board().set_pin_mode_stepper(interface=2, pin1=STEPPER_PULSE_PIN, pin2=STEPPER_DIRECTION_PIN)
        self.external_board().get_board().stepper_set_current_position(0, 0)
        self.external_board().get_board().stepper_set_max_speed(self.stepper, STEPPER_SPEED)
        self.external_board().get_board().stepper_set_speed(self.stepper, STEPPER_SPEED)
        self.external_board().get_board().stepper_set_acceleration(self.stepper, STEPPER_ACCELERATION)

    def send_i2c_packet(self, address: int, payload: list):
        print("I2C> Sending i2c payload at address:", address, "with payload:", payload)
        self.external_board().get_board().i2c_write(address, payload)

    def receive_i2c_packet(self, data):
        print("I2C> Receiving i2c packet payload", data)
        self.last_i2c_response = data
        self.is_waiting_i2c = False

    def resume_last_target(self):
        x = self.get_robot_state()['target_x']
        y = self.get_robot_state()['target_y']
        d = self.get_robot_state()['target_d']
        r = self.get_robot_state()['target_r']

        payloadLinear = [MotorCommands.GOTOLINEAR, int_to_int16(x), int_to_int16(y), int_to_int16(d)]
        self.send_i2c_packet(MOTORCARD_I2C_ADDRESS, payloadLinear)

        payloadRotation = [MotorCommands.GOTOANGLE, int_to_int16(r)]
        self.send_i2c_packet(MOTORCARD_I2C_ADDRESS, payloadRotation)

    def fetch_data_from_i2c(self, motor_command: MotorCommands):
        assert motor_command in [MotorCommands.ERRANGULAR, MotorCommands.ERRLINEAR, MotorCommands.GETPOSITION]
        self.is_waiting_i2c = True
        self.external_board().get_board().i2c_read(MOTORCARD_I2C_ADDRESS, motor_command.value.i2c_cmd, motor_command.value.i2c_response_len, self.receive_i2c_packet)
        while self.is_waiting_i2c:
            time.sleep(0.01)



    def distance_to_goal(self):
        pass
        # call fetch data_from_i2c and extract from last_i2c_response + int16 -> python int

    def goto_position(self, x: int, y: int, forward: bool, r: int, collideAvoidance=True):  # Use -1 if the param is not used
        logging.info(f"I2C> Go to with x={x} y={y} r={r}")

        if x != -1:
            self.get_robot_state()['target_x'] = x
        if y != -1:
            self.get_robot_state()['target_y'] = y
        if r != -1:
            self.get_robot_state()['target_r'] = r

        self.get_robot_state()['target_d'] = 0 if forward else 1

        # while err distance end is gte MIN_DISTANCE_TRESHOLD
        #
            # if collideAvoidance:
            #     while self.robot_state['colliding']['front'] or self.robot_state['colliding']['back']:

#         time.sleep(0.2)

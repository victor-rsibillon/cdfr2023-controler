from enum import Enum
from driver.controller import Controller
from driver.portctrl import PortsController
import logging

motor_card_i2c_address = 83
rotation_avoid_obstacle_step = 45
main_controller = 'ltp3'
ext_controller = 'mega'


def int_to_str16(val: int):
    v = hex((val + (1 << 16)) % (1 << 16))[2:].zfill(4)
    return [v[:2], v[2:]]


def int_to_int16(val: int):
    v = hex((val + (1 << 16)) % (1 << 16))[2:].zfill(4)
    return [int(v[:2], 16), int(v[2:], 16)]


class MotorCommand:
    def __init__(self, name: str, i2c_cmd: int):
        self.name = name,
        self.i2c_cmd = i2c_cmd


class MotorCommands(Enum):
    SETPOSITION = MotorCommand("set_pos", 1)
    LINEAIRE = MotorCommand("goto_linear", 10)
    ANGULAIRE = MotorCommand("goto_linear_curve", 11)
    TOURNERAVANCER = MotorCommand("move_turn_linear", 12)
    TOURNER = MotorCommand("goto_turn", 14)
    STOPMOTOR = MotorCommand("stop", 13)


class Strategy:
    def __init__(self, port_ctrl: PortsController, debug=False):
        self.port_ctrl = port_ctrl
        self.robot_state = None
        self.debug = debug

    def main_board(self) -> Controller:
        return self.port_ctrl.ctrls[main_controller]

    def ext_board(self) -> Controller:
        return self.port_ctrl.ctrls[ext_controller]

    def get_robot_state(self) -> dict:
        return self.robot_state

    def setup_std_pins(self, robot_state: dict):
        self.robot_state = robot_state
        self.main_board().get_board().set_pin_mode_i2c()

    def send_i2c_command(self, address: int, payload: list):
        self.main_board().get_board().i2c_write(address, payload)

    def send_i2c_motor_control(self, cmd: MotorCommands, x: int, y: int, r: int):
        logging.info(f"I2C> Sending i2c packet {cmd.value.name} with x={x} y={y} r={r}")

        if cmd == MotorCommands.LINEAIRE or cmd == MotorCommands.TOURNERAVANCER:  # todo: complete all cases
            while self.robot_state['colliding']['front'] or self.robot_state['colliding']['back']:
                self.send_i2c_command(motor_card_i2c_address,
                                      [MotorCommands.TOURNER.value.i2c_cmd] + int_to_int16(0) + int_to_int16(
                                          0) + int_to_int16(rotation_avoid_obstacle_step))
        payload = [cmd.value.i2c_cmd] + int_to_int16(x) + int_to_int16(y) + int_to_int16(r)
        self.send_i2c_command(motor_card_i2c_address, payload)

    def stop_lidar_collide(self):
        self.send_i2c_motor_control(MotorCommands.STOPMOTOR, 0, 0, 0)

    def update_position_from_odometry(self):
        def position_callback(data):
            logging.error(f"Unhandled position update callback {data}")

        # 50 is the command and 6 is the length of the expected answer
        self.main_board().get_board().i2c_read(motor_card_i2c_address, 50, 6, position_callback)

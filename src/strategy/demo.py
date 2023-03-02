from strategy.shared import *
from driver.portctrl import *
import time


class DemoStrategy(Strategy):
    def __init__(self, port_ctrl: PortsController, debug=False):
        super().__init__(port_ctrl, debug)

    def move(self):
        time.sleep(5)
        super().send_i2c_motor_control(MotorCommands.TOURNERAVANCER, 100, 0, 0)
        # time.sleep(1)
        super().send_i2c_motor_control(MotorCommands.TOURNERAVANCER, -100, 0, 0)
        # time.sleep(1)
        super().send_i2c_motor_control(MotorCommands.TOURNERAVANCER, 0, 0, 0)

    def the_callback(self, data):
        """
        :param data:
        :return:
        """
        print("Incoming i2c payload", data)

    def start(self):
        print("Starting match")

        super().main_board().get_board().set_pin_mode_i2c()
        for i in range(4):
            # read 6 bytes from the data register
            try:
                super().main_board().get_board().i2c_read(42, 50, 1, self.the_callback)
                time.sleep(.001)

            except (KeyboardInterrupt, RuntimeError):
                break
        super().get_robot_state()['grace_full_shutdown'] = True

        # for i in range(4):
        #     a = self.the_callback
        #     print(a)
        #     super().main_board().get_board().i2c_read(42, 50, 8, self.the_callback)
        #     time.sleep(.1)


        # super().send_i2c_motor_control(MotorCommands.TOURNERAVANCER, 100, 0, 0)

        # super().ext_board().get_board().set_pin_mode_analog_output(13)
        # super().ext_board().get_board().analog_write(13, 0)
        #
        # for i in range(1000):
        #     if super().get_robot_state()['colliding_front'] or super().get_robot_state()['colliding_back']:
        #         ratio = int((500 - super().get_robot_state()['colliding_distance']) / 500 * 255)
        #         super().ext_board().get_board().digital_write(13, ratio)
        #     else:
        #         super().ext_board().get_board().analog_write(13, 0)
        #     time.sleep(0.1)

from telemetrix import telemetrix
import asyncio

ALLOWED_REMOTES_CTRL = ['autoDetectCOM', 'manualCOM', 'ethernet']
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3


def default_cb(data):
    print(f"Unhandled pin callback (Pin Mode: {data[CB_PIN_MODE]} Pin: {data[CB_PIN]} Value: {data[CB_VALUE]})")


class Port:
    def __init__(self, raw_port: str):
        sp = raw_port.replace('\n', '').split(";")
        assert len(sp) == 6
        self.device, self.direction, self.port, self.port_id, self.mode, self.desc = sp
        self.board = None
        self.callback = default_cb
        self.port_id = int(self.port_id)
        self.loop = asyncio.get_event_loop()

    def set_parent_board(self, controller):
        self.board = controller

    def register_state(self):
        match self.mode:
            case "gpio_digital_in":
                self.board.set_pin_mode_digital_input_pullup(self.port_id, self.callback)
            case "gpio_analog_in":
                self.board.set_pin_mode_analog_input(self.port_id, 0, self.callback)
            case "gpio_digital_out":
                self.board.set_pin_mode_analog_output(self.port_id)
            case "gpio_analog_out":
                self.board.set_pin_mode_digital_output(self.port_id)

    def update_cb_method(self, callback_function):
        self.callback = callback_function

    def __getitem__(self, item):
        match item:
            case "device":
                return self.device
            case "direction":
                return self.direction
            case "port":
                return self.port
            case "port_id":
                return self.port_id
            case "mode":
                return self.mode


class Controller:
    def __init__(self, ctrl_object: dict):
        self.name = ctrl_object['name']
        self.desc = ctrl_object['desc'] if "desc" in ctrl_object else "No device description specified"
        self.device = ctrl_object['device']
        assert self.device["type"] in ALLOWED_REMOTES_CTRL
        self.portLabel = ctrl_object["portLabel"]
        self.ports = []
        self.board = None
        print(f"Successfully added controller {self.name} at ({str(self.device)})")
        self.register_telemetrix_connection()

    def register_telemetrix_connection(self):
        match self.device["type"]:
            case "autoDetectCOM":
                self.board = telemetrix.Telemetrix(arduino_instance_id=self.device['id'], arduino_wait=self.device['resetTiming'])
            case "manualCOM":
                self.board = telemetrix.Telemetrix(com_port=self.device['com_port'], arduino_wait=self.device['resetTiming'])
            case "ethernet":
                self.board = telemetrix.Telemetrix(ip_address=self.device['ip'], ip_port=self.device['port'], arduino_wait=self.device['resetTiming'])


    def get_board(self):
        return self.board

    def disconnect_board(self):
        print(f"Disconnecting telemtrix board {self.name}")
        if self.board is not None:
            self.board.shutdown()

    def add_port(self, port: Port):
        self.ports.append(port)

    def __getitem__(self, item):
        match item:
            case "name":
                return self.name
            case "device":
                return self.device
            case "portLabel":
                return self.portLabel
            case _:
                return None

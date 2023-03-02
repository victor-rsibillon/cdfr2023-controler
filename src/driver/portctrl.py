import os
from driver.controller import *


class PortsController:
    def __init__(self):
        self.ctrl_obj = None
        self.ctrls = {}

    def set_controlers_config(self, ctrl_obj: dict):
        self.ctrl_obj = ctrl_obj

    def initialize_controlers(self):
        print(f"Ctrl> Attempt to load {len(self.ctrl_obj['interfaces'])} controllers")
        for interface in self.ctrl_obj['interfaces']:
            if interface['enabled']:
                self.register_controller(interface)

        print(f"Ctrl> Linking I/O ports table with current controller")
        self.registers_port(self.ctrl_obj["portTable"])

        return len(self.ctrls)

    def register_controller(self, ctrl_object: dict) -> bool:
        assert "name" in ctrl_object and "device" in ctrl_object and "portLabel" in ctrl_object
        print(f"Ctrl> Attempt to register {ctrl_object['name']} matching {ctrl_object['portLabel']}")
        self.ctrls[ctrl_object['key']] = Controller(ctrl_object)
        return True

    def get(self, key):
        return self.ctrls[key]

    def release_child_controller(self):
        for controller in self.ctrls:
            self.ctrls[controller].disconnect_board()

    def registers_port(self, source_path: str):
        if not os.path.isfile(source_path):
            raise Exception(f"Pinout> Config file({source_path}) is unreadable/not present")

        with open(source_path, 'r') as rawFile:
            lines = rawFile.readlines()[1:]

            for line in lines:
                parsed_port = Port(line)
                guessed_ctrl = list(
                    filter(lambda c: c['portLabel'] == parsed_port['device'], [self.ctrls[ctrl] for ctrl in self.ctrls]))
                if len(guessed_ctrl) == 1:
                    guessed_ctrl[0].add_port(parsed_port)
                    parsed_port.set_parent_board(guessed_ctrl[0])
                else:
                    print(
                        f"Pinout> Attempt to add a I/O but its controller {parsed_port['portLabel']} is not registered")

import os
import json
import driver.controller as ctrl


class PortsController:
    def __init__(self):
        self.ctrls = []

    def addControllers(self, ctrlPath: str):
        if not os.path.isfile(ctrlPath):
            raise Exception(f"Controller config file({ctrlPath}) is unreadabel/not present")

        with open(ctrlPath) as ctrlRaw:
            ctrlObj = json.loads('\n'.join(ctrlRaw.readlines()))
            print(f"Ctrl> Attempt to load {len(ctrlObj['interfaces'])} controllers")
            for interface in ctrlObj['interfaces']:
                self.registerController(interface)

            print(f"Ctrl> Linking I/O ports table with current controller")
            self.registersPort(ctrlObj["portTable"])

        return len(self.ctrls)

    def registerController(self, ctrlObject: dict) -> bool:
        assert "name" in ctrlObject and "device" in ctrlObject and "portLabel" in ctrlObject
        print(f"Ctrl> Attempt to register {ctrlObject['name']} matching {ctrlObject['portLabel']}")
        self.ctrls.append(ctrl.Controller(ctrlObject))
        return True

    def registersPort(self, sourcePath: str):
        if not os.path.isfile(sourcePath):
            raise Exception(f"Pinout> Config file({sourcePath}) is unreadabel/not present")

        with open(sourcePath, 'r') as rawFile:
            lines = rawFile.readlines()[1:]

            for line in lines:
                parsedPort = ctrl.Port(line)
                guessedCtrl = list(filter(lambda c: c['portLabel'] == parsedPort['device'], self.ctrls))
                if len(guessedCtrl) == 1:
                    guessedCtrl[0].addPort(parsedPort)
                    parsedPort.setParentBoard(guessedCtrl[0])
                else:
                    print(f"Pinout> Attempt to add a I/O but its controller {parsedPort['portLabel']} is not registered")

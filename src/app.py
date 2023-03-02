import json
import multiprocessing as mp
import os
import signal
import logging.handlers
import time
from utils import *

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

import driver.portctrl as port_controller
import src.vision.tcpctrl as machine_vision
import vision.lidar as lidar_controller
from strategy.demo import DemoStrategy

latte_panda_core = 4

port_ctrl = port_controller.PortsController()
m_vision_ctrl = None
lidar_ctrl = None
config = {}
processes = []
pool = None
current_strategy = None


def load_config(ctrl_path: str):
    global config
    if not os.path.isfile(ctrl_path):
        raise Exception(f"Controller config file({ctrl_path}) is unreadable/not present")

    with open(ctrl_path) as ctrlRaw:
        config = json.loads('\n'.join(ctrlRaw.readlines()))


def strategy_process(context: dict):
    logging.info("Proc> Starting strategy child process environment")
    port_ctrl.initialize_controlers()
    current_strategy.setup_std_pins(context)
    current_strategy.start()


def machine_vision_process(context: dict):
    logging.info("Proc> Starting machine vision child process environment")
    m_vision_ctrl.init_connection()


def lidar_process(context: dict):
    logging.info("Proc> Starting lidar child process environment")
    lidar_ctrl.setup_connection(context)


def stop_handler(signum, frame):
    logging.error('Signal handler called with signal', signum)
    robot_state['grace_full_shutdown'] = True
    time.sleep(1)
    for p in processes:
        p.terminate()

    # Stopping controller
    port_ctrl.release_child_controller()

    # if enabled_features['machine_vision']:
    #     m_vision_ctrl.close_connection()  # Stopping machine vision


features = {
    'lidar': {
        'enabled': True,
        'handler': lidar_process
    },
    'machine_vision': {
        'enabled': False,
        'handler': machine_vision_process
    },
    'strategy': {
        'enabled': True,
        'handler': strategy_process
    },
}

if __name__ == "__main__":
    load_config("./cfg/master.json")
    assert config is not None

    manager = mp.Manager()
    robot_state = manager.dict()
    default_config(robot_state)

    logging.info("Importing I/O controller from config file (1/3)")
    port_ctrl.set_controlers_config(config)

    logging.info("Configuring tcp socket for machine vision from config file (2/3)")
    m_vision_ctrl = machine_vision.VisionListener(config['machineVision']['host'], config['machineVision']['port'])

    logging.info("Configuring lidar for machine vision from config file (3/3)")
    lidar_ctrl = lidar_controller.LidarSensor(config['lidar']['port'], config['lidar']['baud_rate'])

    logging.info("Initializing strategy instance file")
    current_strategy = DemoStrategy(port_ctrl, True)

    # Detect stop for proper exit
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGABRT, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)

    # Launch individual process
    for feature in features:
        props = features[feature]
        if not props['enabled']:
            continue
        processes.append(mp.Process(target=props['handler'], args=(robot_state,)))

    [p.start() for p in processes]
    [p.join() for p in processes]

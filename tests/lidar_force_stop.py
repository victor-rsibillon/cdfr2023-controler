import sys
from lidar_lib import RPLidar
import time

PORT_NAME = 'COM7'

if __name__ == '__main__':
    lidar = RPLidar(PORT_NAME, baudrate=256000)
    lidar.start_motor()
    print('Connected')
    time.sleep(20)
    print('Stop !')
    lidar.stop_motor()
    time.sleep(0.5)
    print('Disconnect')
    lidar.disconnect()

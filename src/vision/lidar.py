import logging

from vision.lidar_lib import RPLidar
import numpy as np

opening_detection_half_angle = 30
distance_treshold = 500
max_cycle_count = 5


class LidarSensor:
    def __init__(self, port_name: str, baud_rate: int):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.lidar = None
        self.isCollidingFront = False
        self.isCollidingBack = False
        self.shortest_distance = float('inf')
        self.robot_state = None
        self.data = np.full((1, 360), float('inf'))

    def setup_connection(self, handler):
        self.lidar = RPLidar(self.port_name, baudrate=self.baud_rate)
        print(f"Lidar> Device information: {self.lidar.get_info()}")
        print(f"Lidar> Device health: {self.lidar.get_health()}")
        self.robot_state = handler
        self.record_data()

    def record_data(self):
        for scans in self.lidar.iter_scans():
            if self.robot_state['grace_full_shutdown']:
                break
            self.data = np.full((1, 360), float('inf'))
            self.isCollidingFront = False
            self.isCollidingBack = False
            self.shortest_distance = float('inf')
            for scan in scans:
                angle = int(scan[1])
                distance = scan[2]
                self.data[0][angle] = distance

                if 90 - opening_detection_half_angle <= angle <= 90 + opening_detection_half_angle:
                    if distance < distance_treshold:
                        self.isCollidingFront = True
                        self.shortest_distance = distance

                if 270 - opening_detection_half_angle <= angle <= 270 + opening_detection_half_angle:
                    if distance < distance_treshold:
                        self.isCollidingBack = True
                        self.shortest_distance = distance

            self.robot_state['colliding_front'] = self.isCollidingFront
            self.robot_state['colliding_back'] = self.isCollidingBack

            self.robot_state['colliding_distance'] = self.shortest_distance

        self.disconnect_lidar()

    def disconnect_lidar(self):
        self.lidar.stop_motor()
        self.lidar.stop()
        self.lidar.disconnect()

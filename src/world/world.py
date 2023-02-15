import numpy as np

from robot import *


class World:
    def __init__(self):
        self.entities = []
        # Matrix with cell of 10cm by 10cm representing availability of each area (subject to collision)
        self.obstacles = np.zeros((int(TABLE_WIDTH / 100), int(TABLE_HEIGHT / 100)))

    def update_entity_machine_vision(self):
        return None #Todo

    def add_entity(self, entity: Entity) -> int:
        entity.set_id(len(self.entities))
        self.entities.append(entity)
        return len(self.entities) - 1

    def move_robot_to(self, robot: Robot) -> Path:
        return None #Todo





from coord import *


class Entity:
    def __init__(self, name: str, coord: Coordinate, angle=0):
        self.id = -1
        self.name = name
        self.coord = coord
        self.angle = angle

    def set_id(self, id: int):
        self.id = id

    def delta_movement(self, x_delta: int, y_delta: int):
        self.coord.translate(x_delta, y_delta)

    def set_angle(self, angle: int) -> int:
        self.angle = angle % 360
        return self.angle

    def get_angle(self) -> int:
        return self.angle

    def rotate_angle(self, delta_angle) -> int:
        self.angle = (self.angle + delta_angle) % 360
        return self.angle

    def __str__(self):
        return f"Entity(id={self.id}, name={self.name}, coord={self.coord}, angle={self.angle})"

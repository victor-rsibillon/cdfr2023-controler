import math

"""

Conventions used:
- Length are in millimeter no decimal and angle in degrees
- (0;0) at the center of the table
- 0°deg is aiming at the camera pole
- (+,+) is at the the top right corner with the table in horizontal format and the camera pole on the left 

"""
TABLE_WIDTH = 3000
TABLE_HEIGHT = 2000


class Coordinate:
    def __init__(self, x: int, y: int, z=0):
        self.x = x
        self.y = y
        self.z = z
        assert self.is_valid()

    def is_valid(self) -> bool:
        return - TABLE_WIDTH / 2 <= self.x <= TABLE_WIDTH / 2 and -TABLE_HEIGHT / 2 <= self.y <= TABLE_HEIGHT / 2

    def translate(self, x_offset: int, y_offset: int):
        self.x += x_offset
        self.y += y_offset
        assert self.is_valid()

    def distance_to(self, target):
        return math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)

    def __str__(self):
        return f"({self.x};{self.y})"
    def __getitem__(self, item):
        match item:
            case "x":
                return self.x
            case "y":
                return self.y
            case "z":
                return self.z


class Segment:
    def __init__(self, p1: Coordinate, p2: Coordinate):
        self.p1 = p1
        self.p2 = p2

    def get_length(self) -> float:
        return math.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

    def __str__(self):
        return f"{str(self.p1)} -> {str(self.p2)}"

class Path:

    def __init__(self, steps=None):
        if steps is None:
            steps = []
        self.steps = steps

    def get_steps_number(self):
        return len(self.steps)

    def add_steps(self, new_step: Coordinate):
        self.steps.append(new_step)

    def get_total_length(self):
        counter: float = 0
        for coord in self.steps:
            counter += coord.dis
        return counter

    def __str__(self):
        return f"[{','.join([f'({str(segment)})' for segment in self.segments])}]"

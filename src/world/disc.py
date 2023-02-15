from entity import *

"""

Color discs naming convention (from bottom to top):
0 brown 
1 yellow
2 pink

"""


class Disc(Entity):
    def __init__(self, name: str, coord: Coordinate, color: int):
        super().__init__(name, coord)
        assert color in [0, 1, 2]
        self.color = color


class DiscStacking(Entity):

    def __init__(self, name: str, coord: Coordinate):
        super().__init__(name, coord)
        self.layer = {
            0: None,
            1: None,
            2: None
        }

    def is_full(self) -> bool:
        return self.layer[0] is not None and self.layer[1] is not None and self.layer[2] is not None


from world.entity import *


class Robot(Entity):

    def __init__(self, name: str, coord: Coordinate, is_friend: bool, numeral: int):
        super().__init__(name, coord)
        self.is_friend = is_friend
        assert numeral in [0, 1]
        self.numeral = numeral

""" Holds all important constants that define the game's behaviour """

import math
from typing import Union


class WorldConfig:

    @staticmethod
    def builder():
        return WorldConfigBuilder()

    def __init__(self, params):
        self.width: int = params["width"]

        self.friction: Union[int, float] = params["friction"]

        self.flags_ammount: int = params["ammounts"][0]
        self.flags_start: int = params["flags"][0]
        self.flags_distance_in_between: int = params["flags"][1]
        # self.flags_margin_horizontal: int = params["flags"][2]
        self.flags_spacing_vertical: int = params["flags"][3]

        self.trees_ammount: int = params["ammounts"][1]
        self.trees_margin_to_flags: int = params["trees_margin_to_flags"]

        self.flags_left_min: int = params["flags"][2]
        self.flags_left_max: int = self.width - self.flags_distance_in_between - self.flags_left_min

        self.is_downhill: bool = self.flags_ammount == 0
        self.is_slalom: bool = not self.is_downhill

        self.height: int = params["height"] or 1.5 * self.flags_start + (self.flags_ammount - 1) * self.flags_spacing_vertical

        self.time_factor: float = 0.001 * params["difficulty"]
        self.gravity: float = params["gravity"] * math.sin(math.radians(params["inclination"]))


class WorldConfigBuilder:
    def __init__(self):
        # self.width = 800
        # self.height = 0

        # self.difficulty = 1
        # self.gravity = 100
        # self.inclination = 60
        # self.friction = 0.4

        # # [start, distance_between_flags, margin_horizontal, margin_vertical]
        # self.flags = [300, 200, 100, 250]
        # self.trees_margin_to_flags = 50

        # # [flag_pairs, trees]
        # self.ammounts = [20, 50]

        self.width = 0
        self.height = 0

        self.difficulty = 0
        self.gravity = 0
        self.inclination = 0
        self.friction = 0.0

        # [start, distance_between_flags, margin_horizontal, margin_vertical]
        self.flags = [0, 0, 0, 0]
        self.trees_margin_to_flags = 0

        # [flag_pairs, trees]
        self.ammounts = [0, 0]

    def set_width(self, width: int):
        self.width = width
        return self

    def set_height(self, height: int):
        """ If height == 0, the height will be calculated automatically """
        self.height = height
        return self

    def set_difficulty(self, difficulty: int):
        assert difficulty > 0
        self.difficulty = difficulty
        return self

    def set_gravity(self, gravity: Union[float, int]):
        assert gravity > 0
        self.gravity = gravity
        return self

    def set_inclination(self, inclination: Union[float, int]):
        assert 0 < inclination < 90
        self.inclination = inclination
        return self

    def set_friction(self, friction: Union[float, int]):
        assert 0 <= friction < 1
        self.friction = friction
        return self

    def set_flags_start(self, start: int):
        assert start > 0
        self.flags[0] = start
        return self

    def set_distance_between_flags(self, distance: int):
        assert distance > 0
        self.flags[1] = distance
        return self

    def set_flags_margin_horizontal(self, margin_horizontal: int):
        assert margin_horizontal >= 0
        self.flags[2] = margin_horizontal
        return self

    def set_flags_margin_vertical(self, margin_vertical: int):
        assert margin_vertical > 0
        self.flags[3] = margin_vertical
        return self

    def set_flags_ammount(self, ammount: int):
        assert ammount > 0
        self.ammounts[0] = ammount
        return self

    def set_trees_margin_to_flags(self, margin_horizontal: int):
        assert margin_horizontal >= 0
        self.trees_margin_to_flags = margin_horizontal
        return self

    def set_trees_ammount(self, ammount: int):
        assert ammount >= 0
        self.ammounts[1] = ammount
        return self

    def build(self):
        return WorldConfig(self.__dict__)

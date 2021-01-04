""" Holds all logic related to the game's camera (the player's perspective) """

from pygame import Vector2, Surface

from game.types import Number, Vector

class Camera:
    """ This class is responsible for transforming an absolute position into a position that is relative to something it is tracking """
    def __init__(self, screen: Surface, top: Number, padding: Number):
        self.screen = screen
        self.top = top
        self.padding = padding
        self.offset = 0

    def track(self, pos: Vector):
        y = pos[1]
        self.offset = -y + min(y + self.padding, self.top)

    def transform(self, vector: Vector):
        return Vector2(vector[0], vector[1] + self.offset)

    def blit(self, surface: Surface, dest: Vector):
        return self.screen.blit(surface, self.transform(dest))

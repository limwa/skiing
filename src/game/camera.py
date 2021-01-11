""" Holds all logic related to the game's camera (the player's perspective) """

from pygame import Vector2, Surface, Rect

from game.types import Number, Vector

class Camera:
    """ This class is responsible for transforming an absolute position into a position that is relative to something it is tracking """
    def __init__(self, screen: Surface, top: Number, padding: Number):
        self.screen = screen
        self.top = top
        self.padding = padding
        self.offset = 0

    def track(self, pos: Vector):
        self.offset = -pos[1] + min(pos[1] + self.padding, self.top)

    def transform(self, vector: Vector):
        return Vector2(vector[0], vector[1] + self.offset)

    def blit(self, surface: Surface, dest: Vector):
        return self.screen.blit(surface, self.transform(dest))

""" Holds all logic related to the game's camera (the player's perspective) """


from multipledispatch import dispatch

from pygame import Vector2, Surface

from config import COORDINATE, VECTOR

class Camera:
    """ This class is responsible for transforming an absolute position into a position that is relative to something it is tracking """
    @dispatch(Surface, COORDINATE, COORDINATE)
    def __init__(self, screen, top, padding):
        self.screen = screen
        self.top = top
        self.padding: float = padding
        self.offset = 0

    @dispatch(COORDINATE)
    def track(self, y):
        self.offset = -y + min(y + self.padding, self.top)

    @dispatch(VECTOR)
    def track(self, pos):
        self.track(pos[1])

    @dispatch(COORDINATE, COORDINATE)
    def transform(self, x, y) -> Vector2:
        return Vector2(x, y + self.offset)

    @dispatch(VECTOR)
    def transform(self, vector) -> Vector2:
        return self.transform(vector[0], vector[1])

    @dispatch(Surface, VECTOR)
    def blit(self, surface, dest):
        return self.screen.blit(surface, self.transform(dest))
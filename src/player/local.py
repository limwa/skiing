""" Holds all logic related to a local player """

import math
from multipledispatch import dispatch

import pygame.sprite
from pygame import Vector2

from config import WIDTH, PLANE_ACCELERATION, FRICTION_CONSTANT
from camera import Camera


class PlayerLocal(pygame.sprite.Sprite):
    """ Represents a local player in the game """

    @staticmethod
    def init(states):
        PlayerLocal.__states = states

    @dispatch(Vector2, Vector2)
    def __init__(self, pos, velocity):
        pygame.sprite.Sprite.__init__(self)

        self.pos: Vector2 = pos
        self.velocity: Vector2 = velocity

        self.state = len(self.__states) // 2
        self.rect.center = self.pos

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, s: int):
        # We need the state to be valid at all times
        s = max(s, 0)
        s = min(s, len(self.__states) - 1)

        self.__state = s

        data = self.__states[s]

        self.__angle = data[0]
        self.__angle_rad = math.radians(self.__angle)

        # rotate velocity towards the new direction
        self.velocity = self.velocity.length() * Vector2(math.sin(self.__angle_rad), math.cos(self.__angle_rad))

        self.image, self.rect = data[1]

    @property
    def acceleration(self) -> Vector2:
        return Vector2(
            0.5 * PLANE_ACCELERATION * math.sin(2 * self.__angle_rad),
            PLANE_ACCELERATION * math.cos(self.__angle_rad) ** 2
        ) - FRICTION_CONSTANT * self.velocity  # type: ignore

    @dispatch(float)
    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.pos += self.velocity * dt

        # We need to cap the horizontal component of the position vector
        # to the interval [w / 2, WIDTH - w / 2],
        # where w is the width of the image,
        # so that the player doesn't fall off the screen
        if not self.rect.w / 2 <= self.pos.x <= WIDTH - self.rect.w / 2:
            self.pos.x = max(self.rect.w / 2, self.pos.x)
            self.pos.x = min(WIDTH - self.rect.w / 2, self.pos.x)
            self.velocity.x = 0

        self.rect.center = self.pos  # type: ignore

    @dispatch(Camera)
    def render(self, camera):
        camera.blit(self.image, self.rect)  # type: ignore
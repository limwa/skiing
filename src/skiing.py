#!/usr/bin/env python3
"""
@author: limwa
"""

import os

import math
from typing import List, Tuple, Union

from pygame import Vector2

import pygame
import pygame.locals
import pygame.display
import pygame.image
import pygame.event
import pygame.sprite
import pygame.time
import pygame.draw
import pygame.transform


# EDIT THESE CONSTANTS AT YOUR WILL
# SCREEN CONSTANTS
WIDTH = 800
HEIGHT = 600

# TIME CONSTANTS
TIME_ADJUST = 0.001  # conversion of ms to s
DIFICULTY_MULTIPLIER = 2
assert DIFICULTY_MULTIPLIER > 0

# ENVIRONMENT CONSTANTS
G = math.pi ** math.pi
PLANE_INCLINATION = 60  # inclination of the plane in degrees
FRICTION_CONSTANT = 0.25  # must be lower than 1
assert G > 0
assert 0 < PLANE_INCLINATION < 90
assert 0 <= FRICTION_CONSTANT <= 30

# CAMERA CONSTANTS
CAMERA_PADDING = 50
CAMERA_TRACKING_BOUND = 100
assert CAMERA_TRACKING_BOUND >= CAMERA_PADDING


# DON'T EDIT ANYTHING ELSE


TIME_SCALAR = DIFICULTY_MULTIPLIER * TIME_ADJUST
PLANE_ACCELERATION = G * math.sin(math.radians(PLANE_INCLINATION))

# ASSETS
ROOT = os.path.join(os.path.dirname(__file__), '..')
ASSETS = os.path.join(ROOT, 'assets')


def load_image(name: str):
    """ Loads an image from the assets folder. """

    path = os.path.join(ASSETS, name)
    img = pygame.image.load(path)
    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()

    return img, img.get_rect()
###

# GAME LOGIC
class Camera:
    def __init__(self, top: float, padding: float):
        self.top = top
        self.padding = padding
        self.offset = 0

    def track(self, pos: Vector2) -> None:
        self.offset = -pos.y + min(pos.y + self.padding, self.top)

    def transform(self, vector: Union[Vector2, Tuple[float, float], List[float]]) -> Vector2:
        return Vector2(vector[0], vector[1] + self.offset)


class Skier(pygame.sprite.Sprite):
    """ Represents a Skiier (player) in the game """

    @staticmethod
    def init(states: List[Tuple[float, Tuple[pygame.Surface, pygame.Rect]]]):
        Skier.__states = states

    def __init__(self, pos: Vector2, velocity: Vector2) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.velocity = velocity

        self.__angle = 0
        self.state = len(self.__states) // 2

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

    def update(self, dt: float) -> None:
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

        print(self.velocity, self.pos)

        self.rect.center = self.pos  # type: ignore

    def render(self, screen: pygame.Surface, camera: Camera) -> None:
        screen.blit(self.image, camera.transform(self.rect.topleft))  # type: ignore


def main():
    """ Handles the game startup. """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Skiing by limwa')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((245, 245, 245))

    assets = {i[:-4]: load_image(i) for i in os.listdir(ASSETS)}

    def get_img_and_rect(img): return img, img.get_rect()
    Skier.init([
        (-90, assets["skier-3"]),
        (-60, assets["skier-2"]),
        (-30, assets["skier-1"]),
        (-15, assets["skier-0"]),
        (0, assets["skier-0"]),
        (0, get_img_and_rect(pygame.transform.flip(assets["skier-0"][0], True, False))),
        (15, get_img_and_rect(pygame.transform.flip(assets["skier-0"][0], True, False))),
        (30, get_img_and_rect(pygame.transform.flip(assets["skier-1"][0], True, False))),
        (60, get_img_and_rect(pygame.transform.flip(assets["skier-2"][0], True, False))),
        (90, get_img_and_rect(pygame.transform.flip(assets["skier-3"][0], True, False)))
    ])  # type: ignore

    player = Skier(Vector2(WIDTH / 2, 0), Vector2(0, 0))
    camera = Camera(CAMERA_TRACKING_BOUND, CAMERA_PADDING)

    clock = pygame.time.Clock()
    running = True
    while True:
        dt = clock.tick(60) * TIME_SCALAR

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
                break

            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_RIGHT:
                    player.state += 1
                elif event.key == pygame.locals.K_LEFT:
                    player.state -= 1

        if not running:
            break

        player.update(dt)
        camera.track(player.pos)  # type: ignore

        screen.blit(background, (0, 0))
        player.render(screen, camera)  # type: ignore

        for i in range(200):
            pygame.draw.line(screen, (0, 0, 0), camera.transform(
                (10, i * 100)), camera.transform((WIDTH - 10, i * 100)), 2)

        pygame.display.flip()
###


if __name__ == '__main__':
    main()

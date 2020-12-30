#!/usr/bin/env python3
"""
@author: limwa
"""

import os
import math
import random

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

from multipledispatch import dispatch

from typing import List, Tuple, Union

# EDIT THESE CONSTANTS AT YOUR WILL
# SCREEN CONSTANTS
WIDTH = 800
HEIGHT = 600

# TIME CONSTANTS
TIME_ADJUST = 0.001  # conversion of ms to s
DIFICULTY_MULTIPLIER = 1
assert DIFICULTY_MULTIPLIER > 0

# ENVIRONMENT CONSTANTS
G = 100
PLANE_INCLINATION = 60  # inclination of the plane in degrees
FRICTION_CONSTANT = 0.4  # must be lower than 1
assert G > 0
assert 0 < PLANE_INCLINATION < 90
assert 0 <= FRICTION_CONSTANT < 1

# CAMERA CONSTANTS
CAMERA_PADDING = 50
CAMERA_TRACKING_BOUND = 100
assert CAMERA_TRACKING_BOUND >= CAMERA_PADDING

# FLAG HORIZONTAL CONSTANTS
FLAG_PADDING = 100
FLAG_SPACING_HORIZONTAL = 200

# FLAG VERTICAL CONSTANTS
FLAGS_START = 300
FLAGS_SPACING_VERTICAL = 250


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

# TYPES

COORDINATE = (int, float)
VECTOR = (list, tuple, Vector2, pygame.Rect)

###

# GAME LOGIC
class Camera:

    @dispatch(pygame.Surface, COORDINATE, COORDINATE)
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

    @dispatch(pygame.Surface, VECTOR)
    def blit(self, surface, dest):
        return self.screen.blit(surface, self.transform(dest))


class Skier(pygame.sprite.Sprite):
    """ Represents a Skiier (player) in the game """

    @staticmethod
    def init(states: List[Tuple[float, Tuple[pygame.Surface, pygame.Rect]]]):
        Skier.__states = states

    @dispatch(Vector2, Vector2)
    def __init__(self, pos, velocity):
        pygame.sprite.Sprite.__init__(self)

        self.pos: Vector2 = pos
        self.velocity: Vector2 = velocity

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


def main():
    """ Handles the game startup. """

    pygame.init()
    assert pygame.get_init(), "Pygame could not be initialized."

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Skiing by limwa')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((245, 245, 245))

    assets = {i[:-4]: load_image(i) for i in os.listdir(ASSETS)}

    scaled_flag = pygame.transform.scale(assets["flag"][0], (31, 42))
    assets["flag"] = scaled_flag, scaled_flag.get_rect()
    assets["flag"][1].bottomright = (0, 0)

    scaled_tree = pygame.transform.scale(assets["tree"][0], (85, 82))
    assets["tree"] = scaled_tree, scaled_tree.get_rect()
    assets["tree"][1].bottomleft = (0, 0)

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
    camera = Camera(screen, CAMERA_TRACKING_BOUND, CAMERA_PADDING)

    def generate_flag(y):
        x_start = random.randint(FLAG_PADDING, WIDTH - FLAG_SPACING_HORIZONTAL - FLAG_PADDING)
        x_end = x_start + FLAG_SPACING_HORIZONTAL
        return (assets["flag"][1].move(x_start, y), assets["flag"][1].move(x_end, y))

    flags = [generate_flag(FLAGS_START + i * FLAGS_SPACING_VERTICAL) for i in range(20)]

    def generate_tree():
        y = random.randrange(FLAGS_START, FLAGS_START + 19 * FLAGS_SPACING_VERTICAL)
        prev_flag_index = (y - FLAGS_START) // FLAGS_SPACING_VERTICAL
        prev_flag = flags[prev_flag_index]
        next_flag = flags[prev_flag_index + 1]
        min_x = min(prev_flag[0][0], next_flag[0][0]) - assets["tree"][1].width - 50
        max_x = max(prev_flag[1][0], next_flag[1][0]) + 50

        x = random.randint(0, WIDTH - max_x + min_x)
        if x >= min_x:
            x += max_x - min_x

        return assets["tree"][1].move(x, y)

    trees = [generate_tree() for i in range(50)]

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

        player.render(camera)  # type: ignore

        for flag in flags:
            screen.blit(assets["flag"][0], camera.transform(flag[0]) + assets["flag"][1].topleft) # type: ignore
            screen.blit(assets["flag"][0], camera.transform(flag[1]) + assets["flag"][1].topleft) # type: ignore
            # pygame.draw.line(screen, (0, 0, 0), camera.transform(flag[0]), camera.transform(flag[1]), 2)

        for tree in trees:
            screen.blit(assets["tree"][0], camera.transform(tree) + assets["tree"][1].topleft) # type: ignore

        # for tree in trees:
        #     pygame.draw.circle(screen, (0, 0, 0), camera.transform(tree), 2, 3)
        pygame.display.flip()

###


if __name__ == '__main__':
    main()

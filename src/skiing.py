#!/usr/bin/env python3
"""
@author: limwa
"""

import os
import sys

from typing import List, Tuple

import pygame
import pygame.locals
import pygame.display
import pygame.image
import pygame.event
import pygame.sprite
import pygame.time

WIDTH = 800
HEIGHT = 600

DIFICULTY_MULTIPLIER = 1
TIME_ADJUST = 0.1

ROOT = os.path.join(os.path.dirname(__file__), '..')
ASSETS = os.path.join(ROOT, 'assets')

def load_image(name):
    """ Loads an image from the assets folder. """

    path = os.path.join(ASSETS, name)
    img = pygame.image.load(path)
    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()

    return img

class Skier(pygame.sprite.Sprite):
    """ Represents a Skiier (player) in the game """
    def __init__(self, pos: List[float], velocity: List[float], angle: float, inverted: bool) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.set_velocity(velocity)
        self.set_angle(0, inverted)

        image = load_image('skier-0.png')
        self.image = image
        self.rect = image.get_rect()

    def set_angle(self, angle: float, inverted: bool):
        self.angle = angle
        self.inverted = inverted

    def set_position(self, pos: List[float]):
        self.pos = pos

    def set_velocity(self, velocity: List[float]):
        assert len(velocity) == len(self.pos), 'Length of velocity vector must be equal to that of position vector'
        self.velocity = velocity

    def update(self, dt):
        for i in range(len(self.pos)):
            self.pos[i] += self.velocity[i] * DIFICULTY_MULTIPLIER * TIME_ADJUST * dt

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.pos) # type: ignore


def main():
    """ Handles the game startup. """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Skiing by limwa')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((245, 245, 245))

    player = Skier([WIDTH // 2, 50], [0, 1], 0, False)

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return

            elif event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_DOWN:
                    player.set_velocity([0, 1])
                elif event.key == pygame.locals.K_UP:
                    player.set_velocity([0, -1])

        player.update(dt)

        screen.blit(background, (0, 0))
        player.render(screen) # type: ignore


        pygame.display.flip()

if __name__ == '__main__':
    main()

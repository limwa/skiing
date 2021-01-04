#!/usr/bin/env python3
"""
@author: limwa
"""


import os
import random

import pygame
from pygame import Vector2
import pygame.locals
import pygame.display
import pygame.image
import pygame.event
import pygame.sprite
import pygame.time
import pygame.draw
import pygame.transform

from game.config import WorldConfig
import game.player
import game.camera
import game.landscape


# GAME LOGIC
def main():
    """ Handles the game startup. """

    config = WorldConfig.builder() \
        .set_width(800) \
        .set_difficulty(1) \
        .set_gravity(100) \
        .set_inclination(60) \
        .set_friction(0.4) \
        .set_flags_start(300) \
        .set_distance_between_flags(200) \
        .set_flags_margin_horizontal(100) \
        .set_flags_margin_vertical(250) \
        .set_trees_margin_to_flags(100) \
        .set_flags_ammount(20) \
        .set_trees_ammount(40) \
        .build()

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

    pygame.init()
    assert pygame.get_init(), "Pygame could not be initialized."

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Skiing by limwa')

    game.player.init()

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((245, 245, 245))

    player = game.player.Player(config, Vector2(config.width / 2, 0), Vector2(0, 0))
    camera = game.camera.Camera(screen, 100, 50)
    landscape = game.landscape.LocalLandscape(config)

    def tick(dt):
        player.update(dt)

        # collisions = []

    def render():
        screen.blit(background, (0, 0))

        camera.track(player.pos)

        player.render(camera)
        landscape.render(camera)

        pygame.display.flip()



    clock = pygame.time.Clock()
    waiting = True
    running = True

    render() # We need to wait until the player hits the down key for the game to start
    while running and waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
                break

            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_DOWN:
                    waiting = False
                    break

    # After the player hits the down key, we need to start the game
    while running:
        dt = clock.tick(60) * config.time_factor

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
                break

            player.processEvent(event)

        if not running:
            break

        tick(dt)
        render()
###


if __name__ == '__main__':
    main()

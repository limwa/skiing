#!/usr/bin/env python3
"""
@author: limwa
"""

import pygame
import pygame.locals
import pygame.display
import pygame.event
import pygame.time
import pygame.draw
from pygame import Vector2

from game.config import WorldConfig
import game
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

    landscape = game.landscape.LocalLandscape(config)
    player = game.player.Player(landscape, Vector2(config.width / 2, 0), Vector2(0, 0))

    current_game = game.Game(screen, landscape, player)
    player2 = game.player.Player(landscape, Vector2(0, 0), Vector2(0, 0))
    current_game.add_player(player2)
    current_game.start()

###


if __name__ == '__main__':
    main()

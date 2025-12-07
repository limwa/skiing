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

import game
import game.player
import game.camera
import game.landscape
import game.rendering
from game.config import WorldConfig


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

    pygame.init()
    assert pygame.get_init(), "Pygame could not be initialized."

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Skiing')

    game.player.init()

    renderer = game.rendering.Renderer(screen)
    landscape = game.landscape.LocalLandscape(config)
    player = game.player.Player(landscape, Vector2(config.width / 2, 0), Vector2(0, 0))

    current_game = game.Game(renderer, landscape, player)
    # player2 = game.player.Player(landscape, Vector2(0, 0), Vector2(0, 0))
    # current_game.add_player(player2)
    ended_successfuly = current_game.start()

    if ended_successfuly:
        current_game.game_millis += (config.flags_ammount - current_game.get_main_player().score) * 5000000 * config.time_factor

        clock = pygame.time.Clock()
        while ended_successfuly:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    ended_successfuly = False

            renderer.render(current_game)

    pygame.quit()

###


if __name__ == '__main__':
    main()

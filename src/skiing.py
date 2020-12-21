#!/usr/bin/env python3
"""
@author: limwa
"""

import pygame
import pygame.locals
import pygame.display
import pygame.event
import pygame.image
import pygame.sprite

import os
import sys


WIDTH = 800
HEIGHT = 600

ROOT = os.path.join(os.path.dirname(__file__), '..')
ASSETS = os.path.join(ROOT, 'assets')


def load_image(name):
    """
    Loads an image from the assets folder.
    """

    path = os.path.join(ASSETS, name)
    img = pygame.image.load(path)
    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()

    return img


def main():
    """
    Handles the game startup.
    """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Skiing by limwa')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((245, 245, 245))

    skiers = [load_image(i) for i in ['skier-0.png', 'skier-1.png', 'skier-2.png', 'skier-3.png', 'skier-2.png', 'skier-1.png']]

    i= 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return

        i += 1

        screen.blit(background, (0, 0))
        screen.blit(skiers[(i // 2000) % len(skiers)], (WIDTH // 2 - skiers[(i // 2000) % len(skiers)].get_width() // 2, HEIGHT // 2 - skiers[(i // 2000) % len(skiers)].get_height() // 2))
        pygame.display.flip()

if __name__ == '__main__':
    main()

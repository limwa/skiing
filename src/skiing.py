#!/usr/bin/env python3
"""

@author: limwa
"""

import pygame
from pygame.locals import *

import pygame.display
import pygame.event

WIDTH = 800
HEIGHT = 600

def main():
    """
    Handles the game startup.
    """

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Skiing by limwa')

    background = pygame.Surface(screen.get_size())
    background.convert()
    background.fill((255, 255, 255))
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    main()

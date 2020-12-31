#!/usr/bin/env python3
"""
@author: limwa
"""


import os
import random

import pygame
import pygame.locals
import pygame.display
import pygame.image
import pygame.event
import pygame.sprite
import pygame.time
import pygame.draw
import pygame.transform

from config import *
from player.local import PlayerLocal
from camera import Camera

def load_image(name: str):
    """ Loads an image from the assets folder. """

    path = os.path.join(ASSETS, name)
    img = pygame.image.load(path)
    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()

    return img, img.get_rect()

# GAME LOGIC
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
    PlayerLocal.init([
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

    player = PlayerLocal(Vector2(WIDTH / 2, 0), Vector2(0, 0))
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
            screen.blit(assets["flag"][0], camera.transform(flag[0])) # type: ignore
            screen.blit(assets["flag"][0], camera.transform(flag[1])) # type: ignore
            # pygame.draw.line(screen, (0, 0, 0), camera.transform(flag[0]), camera.transform(flag[1]), 2)

        for tree in trees:
            screen.blit(assets["tree"][0], camera.transform(tree)) # type: ignore

        # for tree in trees:
        #     pygame.draw.circle(screen, (0, 0, 0), camera.transform(tree), 2, 3)
        pygame.display.flip()
###


if __name__ == '__main__':
    main()

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

    ### Let's load all assets
    assets = { i[:-4]: load_image(i) for i in os.listdir(ASSETS) } # load every image from the assets folder

    player_states = []
    for angle, asset in [(0, "skier-0"), (-15, "skier-0"), (-30, "skier-1"), (-60, "skier-2"), (-90, "skier-3")]:
        img_and_rect = assets[asset]
        player_states.insert(0, (angle, img_and_rect))

        flipped = pygame.transform.flip(img_and_rect[0], True, False)
        player_states.append((-angle, (flipped, flipped.get_rect())))

    PlayerLocal.init(player_states)

    flag_img, flag_rect = assets["flag"]
    tree_img, tree_rect = assets["tree"]

    # Alright, we're done with assets
    del assets

    ### Now, let's generate the landscape
    def generate_flag(y):
        x_start = random.randint(FLAG_PADDING, WIDTH - FLAG_SPACING_HORIZONTAL - FLAG_PADDING)
        x_end = x_start + FLAG_SPACING_HORIZONTAL
        return (flag_rect.move(x_start, y), flag_rect.move(x_end, y))

    flags = [generate_flag(FLAGS_START + i * FLAGS_SPACING_VERTICAL) for i in range(20)]

    def generate_tree():
        y = random.randrange(FLAGS_START, FLAGS_START + 19 * FLAGS_SPACING_VERTICAL)
        prev_flag_index = (y - FLAGS_START) // FLAGS_SPACING_VERTICAL
        prev_flag = flags[prev_flag_index]
        next_flag = flags[prev_flag_index + 1]
        min_x = min(prev_flag[0][0], next_flag[0][0]) - tree_rect.width - 50
        max_x = max(prev_flag[1][0], next_flag[1][0]) + 50

        x = random.randint(0, WIDTH - max_x + min_x)
        if x >= min_x:
            x += max_x - min_x

        return tree_rect.move(x, y)

    trees = [generate_tree() for _ in range(50)]
    # What a beautiful landscape, it's finished


    player = PlayerLocal(Vector2(WIDTH / 2, 0), Vector2(0, 0))
    camera = Camera(screen, CAMERA_TRACKING_BOUND, CAMERA_PADDING)

    def tick(dt):
        player.update(dt)

    def render():
        screen.blit(background, (0, 0))

        camera.track(player.pos)
        player.render(camera)

        for flag in flags:
            camera.blit(flag_img, flag[0])
            camera.blit(flag_img, flag[1])

        for tree in trees:
            camera.blit(tree_img, tree)

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

        tick(dt)
        render()
###


if __name__ == '__main__':
    main()

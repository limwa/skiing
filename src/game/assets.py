import os
import pygame.image

from pygame import Surface
from typing import Dict

FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
class Image:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.rect = surface.get_rect()

images: Dict[str, Image] = {}

def get_image(name: str):
    """ Loads an image from the assets folder. """
    if '.' not in name:
        name = name + '.png'

    if name in images:
        return images[name]

    path = os.path.join(FOLDER, name)
    img = pygame.image.load(path)
    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()

    asset = Image(img) # type: ignore
    images[name] = asset
    return asset

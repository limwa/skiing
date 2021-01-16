import os
from typing import Dict, Tuple


import pygame.image
import pygame.font
import pygame.mixer
from pygame import Surface

FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
class Image:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.rect = surface.get_rect()

class Font(pygame.font.Font):
    def __init__(self, path: str, size: int) -> None:
        super().__init__(path, size)

class Sound(pygame.mixer.Sound):
    def __init__(self, path: str) -> None:
        super().__init__(path)

images: Dict[str, Image] = {}
fonts: Dict[Tuple[str, int], Font] = {}
sounds: Dict[str, Sound] = {}

def get_image(name: str):
    """ Loads an image from the assets folder. """
    if '.' not in name:
        name = name + '.png'

    if name in images:
        return images[name]

    path = os.path.join(FOLDER, "images", name)
    img = pygame.image.load(path)
    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()

    image = Image(img) # type: ignore
    images[name] = image
    return image

def get_font(name: str, size: int):
    """ Loads a font from the assets folder. """
    if '.' not in name:
        name = name + '.ttf'

    if (name, size) in fonts:
        return fonts[(name, size)]

    path = os.path.join(FOLDER, "fonts", name)
    font = Font(path, size)
    fonts[(name, size)] = font
    return font

def get_sound(name: str):
    """ Loads a sound from the assets folder. """
    if '.' not in name:
        name = name + '.ogg'

    if name in sounds:
        return sounds[name]

    path = os.path.join(FOLDER, "sounds", name)

    sound = Sound(path) # type: ignore
    sounds[name] = sound
    return sound

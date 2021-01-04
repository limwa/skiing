""" Holds all logic related to players (both local and remote players) """
import math
import random
from typing import List, Tuple, Union

import pygame.sprite
import pygame.draw
import pygame.transform
import pygame.locals
from pygame import Vector2
from pygame.event import Event

import game.assets
from game.config import WorldConfig
from game.camera import Camera

class Keyboard:
    def __init__(self, k_left: int, k_right: int):
        self.k_left = k_left
        self.k_right = k_right
        self.locked = False
        self.lock_secret = -1

    def is_locked(self):
        return self.locked

    def lock(self) -> Union[int, None]:
        if not self.locked:
            self.locked = True
            self.lock_secret = random.randint(0, 2 ** 16)
            return self.lock_secret

        return None

    def unlock(self, lock_secret: int):
        if lock_secret == self.lock_secret:
            self.locked = False

    def is_turning_left(self, event: Event):
        return event.type == pygame.locals.KEYDOWN and event.key == self.k_left

    def is_turning_right(self, event: Event):
        return event.type == pygame.locals.KEYDOWN and event.key == self.k_right

KEYBOARDS = [
    Keyboard(pygame.locals.K_LEFT, pygame.locals.K_RIGHT),
    Keyboard(pygame.locals.K_a, pygame.locals.K_d),
    Keyboard(pygame.locals.K_h, pygame.locals.K_k),
    # Keyboard(pygame.locals.K_KP9)
]

def get_keyboard():
    for keyboard in KEYBOARDS:
        if not keyboard.is_locked():
            return keyboard

    return None

class Player(pygame.sprite.Sprite):
    """ Represents a local player in the game """

    @staticmethod
    def init(states):
        Player.__states = states

    def __init__(self, world: WorldConfig, pos: Vector2, velocity: Vector2, keyboard: Union[Keyboard, None] = None):
        pygame.sprite.Sprite.__init__(self)

        self.world = world
        self.pos = pos
        self.velocity = velocity

        self.state = len(self.__states) // 2

        self.update(0)

        while keyboard is None or keyboard.is_locked():
            keyboard = get_keyboard()

        self.keyboard = keyboard
        self.keyboard_lock_secret = self.keyboard.lock()


    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, s: int):
        # We need the state to be valid at all times
        s = max(s, 0)
        s = min(s, len(self.__states) - 1)

        self.__state = s

        data = self.__states[s]

        self.__angle = data[0]
        self.__angle_rad = math.radians(self.__angle)

        # rotate velocity towards the new direction
        self.velocity = self.velocity.length() * Vector2(math.sin(self.__angle_rad), math.cos(self.__angle_rad))

        self.image, self.rect = data[1].surface, data[1].rect

    @property
    def acceleration(self) -> Vector2:
        return Vector2(
                0.5 * self.world.gravity * math.sin(2 * self.__angle_rad),
                self.world.gravity * math.cos(self.__angle_rad) ** 2
            ) - self.world.friction * self.velocity # type: ignore

    def processEvent(self, event: Event):
        if event.type == pygame.locals.KEYDOWN:
            if self.keyboard.is_turning_left(event):
                self.state -= 1
                return

            if self.keyboard.is_turning_right(event):
                self.state += 1
                return


    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.pos += self.velocity * dt

        # We need to cap the horizontal component of the position vector
        # to the interval [w / 2, WIDTH - w / 2],
        # where w is the width of the image,
        # so that the player doesn't fall off the screen
        if not self.rect.w / 2 <= self.pos.x <= self.world.width - self.rect.w / 2:
            self.pos.x = max(self.rect.w / 2, self.pos.x)
            self.pos.x = min(self.world.width - self.rect.w / 2, self.pos.x)
            self.velocity.x = 0

        self.rect.center = self.pos  # type: ignore

    def render(self, camera):
        camera.blit(self.image, self.rect)  # type: ignore
        pygame.draw.circle(camera.screen, (0, 255, 255), camera.transform(self.rect.center), 2, 1)

def init():
    player_states: List[Tuple[int, game.assets.Image]] = []
    for angle, asset in [(0, "skier-0"), (-15, "skier-0"), (-30, "skier-1"), (-60, "skier-2"), (-90, "skier-3")]:
        image = game.assets.get_image(asset)
        player_states.insert(0, (angle, image))

        flipped = pygame.transform.flip(image.surface, True, False)
        player_states.append((-angle, game.assets.Image(flipped)))

    Player.init(player_states)
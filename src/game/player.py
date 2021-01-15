""" Holds all logic related to players (both local and remote players) """
import math
from uuid import UUID, uuid4
from typing import List, Tuple, Union

import pygame.sprite
import pygame.draw
import pygame.transform
import pygame.locals
from pygame import Vector2, Rect
from pygame.event import Event

import game.assets
from game.camera import Camera
from game.landscape import Tree, Flag, FlagPair, Landscape

class Keyboard:
    def __init__(self, k_left: int, k_right: int):
        self.k_left = k_left
        self.k_right = k_right
        self.locked = False

    def is_locked(self):
        return self.locked

    def lock(self) -> bool:
        if not self.locked:
            self.locked = True
            return True

        return False

    def unlock(self):
        self.locked = False

    def is_turning_left(self, event: Event):
        return event.type == pygame.locals.KEYDOWN and event.key == self.k_left

    def is_turning_right(self, event: Event):
        return event.type == pygame.locals.KEYDOWN and event.key == self.k_right

KEYBOARDS = [
    Keyboard(pygame.locals.K_LEFT, pygame.locals.K_RIGHT),
    Keyboard(pygame.locals.K_a, pygame.locals.K_d),
    Keyboard(pygame.locals.K_h, pygame.locals.K_k),
    Keyboard(pygame.locals.K_KP7, pygame.locals.K_KP9)
]

def get_keyboard():
    for keyboard in KEYBOARDS:
        if not keyboard.is_locked():
            return keyboard

    return None

class Player(pygame.sprite.Sprite):
    """ Represents a local player in the game """

    INVULN_TIME = 4
    DOWN_TIME = 2

    @staticmethod
    def init(states, down):
        Player.__states: List[Tuple[int, game.assets.Image]] = states
        Player.__down: game.assets.Image = down

    def __init__(self, landscape: Landscape, pos: Vector2, velocity: Vector2, uuid: Union[UUID, None] = None, keyboard: Union[Keyboard, None] = None):
        pygame.sprite.Sprite.__init__(self)

        self.uuid = uuid or uuid4()

        self.landscape = landscape
        self.pos = pos
        self.velocity = velocity

        self.state = len(self.__states) // 2
        self.collision_box = Rect(0, 0, 15, 15)
        self.time_since_last_collision = Player.INVULN_TIME

        self.score = 0
        self.last_scored_pair: Union[FlagPair, None] = None

        while keyboard is None or keyboard.is_locked():
            keyboard = get_keyboard()

        self.keyboard = keyboard
        self.keyboard.lock()

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

        self.image, self.rect = data[1].surface, data[1].rect.copy()

    @property
    def acceleration(self) -> Vector2:
        return Vector2(
                0.5 * self.landscape.world.gravity * math.sin(2 * self.__angle_rad),
                self.landscape.world.gravity * math.cos(self.__angle_rad) ** 2
            ) - self.landscape.world.friction * self.velocity # type: ignore

    def process_event(self, event: Event):
        if self.time_since_last_collision < Player.DOWN_TIME:
            return

        if event.type == pygame.locals.KEYDOWN:
            if self.keyboard.is_turning_left(event):
                self.state -= 1
                return

            if self.keyboard.is_turning_right(event):
                self.state += 1
                return

    def update(self, dt: float):
        if self.time_since_last_collision >= Player.DOWN_TIME:
            self.velocity += self.acceleration * dt
            self.pos += self.velocity * dt

            # We need to cap the horizontal component of the position vector
            # to the interval [w / 2, WIDTH - w / 2],
            # where w is the width of the image,
            # so that the player doesn't fall off the screen
            if not self.rect.w / 2 <= self.pos.x <= self.landscape.world.width - self.rect.w / 2:
                self.pos.x = max(self.rect.w / 2, self.pos.x)
                self.pos.x = min(self.landscape.world.width - self.rect.w / 2, self.pos.x)
                self.velocity.x = 0

        self.rect.center = (int(self.pos.x), int(self.pos.y))

        self.time_since_last_collision += dt
        self.collision_box.midbottom = self.rect.center
        self.collision_box.move_ip(0, 5) # Position the collision box in the right place

    def render(self, camera: Camera):
        camera.blit(self.image if self.time_since_last_collision >= Player.DOWN_TIME else Player.__down.surface, self.rect)
        # pygame.draw.rect(camera.screen, (200, 200, 200), Rect(camera.transform(self.collision_box.topleft), (self.collision_box.width, self.collision_box.height)), 2)
        # pygame.draw.circle(camera.screen, (0, 255, 255), camera.transform(self.rect.center), 2, 1)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Player):
            return False

        return o.uuid == self.uuid

    def __hash__(self) -> int:
        return self.uuid.__hash__()


def init():
    player_states: List[Tuple[int, game.assets.Image]] = []
    for angle, asset in [(0, "skier-0"), (-15, "skier-0"), (-30, "skier-1"), (-60, "skier-2"), (-90, "skier-3")]:
        image = game.assets.get_image(asset)
        player_states.insert(0, (angle, image))

        flipped = pygame.transform.flip(image.surface, True, False)
        player_states.append((-angle, game.assets.Image(flipped)))

    Player.init(player_states, game.assets.get_image('skier-4'))


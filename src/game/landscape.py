""" Handles landscape generation and collision checks """

import random
from typing import List, overload
from pygame import Surface, Rect

import game.assets
from game.camera import Camera
from game.config import WorldConfig
from game.types import Vector

class Collidable:
    def __init__(self, collision_box: Rect):
        self.collision_box = collision_box

    @overload
    def collides_at(self, pos) -> bool: ...
    @overload
    def collides_at(self, prev_pos, pos) -> bool: ...

    # def collides_at(self, first, second = None) -> bool:
    #     if second is None:
    #         return bool(self.collision_box.collidepoint(first))

    #     return len(self.collision_box.clipline(first, second)) != 0

    def collides_at(self, first, second = None) -> bool:
        if second is None:
            return bool(self.collision_box.colliderect(first))

        return len(self.collision_box.clipline(first, second)) != 0
class Obstacle(Collidable):
    def __init__(self, image: Surface, rect: Rect, collision_box: Rect):
        assert image.get_width() == rect.width
        assert image.get_height() == rect.height

        super().__init__(collision_box)
        self.image = image
        self.rect = rect

    def render(self, camera: Camera):
        return camera.blit(self.image, self.rect)

class Flag(Obstacle):

    COLLISION_BOX_WIDTH = 10
    def __init__(self, bottomright: Vector):
        image = game.assets.get_image('flag')

        # set the bottom right corner of the Rect at bottomright
        rect = image.rect.move(bottomright[0] - image.rect.width, bottomright[1] - image.rect.height)

        collision_box = Rect(0, 0, Flag.COLLISION_BOX_WIDTH, rect.height)
        collision_box.bottomright = rect.bottomright

        super().__init__(image.surface, rect, collision_box)

class FlagPair(Collidable):

    COLLISION_BOX_HEIGHT = 5
    def __init__(self, world: WorldConfig, y: int, left_x: int):
        self.y = y
        self.left_x = left_x
        self.right_x = left_x + world.flags_distance_in_between

        self.left = Flag((self.left_x, y))
        self.right = Flag((self.right_x, y))

        collision_box = Rect(0, 0, world.flags_distance_in_between, FlagPair.COLLISION_BOX_HEIGHT)
        collision_box.bottomleft = self.left.rect.bottomright

        super().__init__(collision_box)

    def render(self, camera: Camera):
        self.left.render(camera)
        self.right.render(camera)

class Tree(Obstacle):

    COLLISION_BOX_HEIGHT = 5
    def __init__(self, center: Vector):
        image = game.assets.get_image('tree')

        rect = image.rect.copy()
        rect.center = (int(center[0]), int(center[1]))

        collision_box = Rect(0, 0, rect.width, Tree.COLLISION_BOX_HEIGHT)
        collision_box.midbottom = rect.midbottom

        super().__init__(image.surface, rect, collision_box)

class Landscape:
    def __init__(self, world: WorldConfig, flag_pairs: List[FlagPair], trees: List[Tree]):
        # We need to verify if the given landscape is valid.
        # Therefore, we only need to verify the flags list.
        # The flag_pairs array needs to meet one requirement:
        #   - for every flag_pair,
        #    the previous one must have a lower y value.
        for i in range(len(flag_pairs) - 1):
            current_y = flag_pairs[i].y
            next_y = flag_pairs[i + 1].y

            assert current_y < next_y

        self.width = world.width
        self.height = world.height

        self.world = world

        self.flag_pairs = flag_pairs
        self.trees = trees

class LocalLandscape(Landscape):
    def __init__(self, world: WorldConfig):
        def new_flag_pair(y) -> FlagPair:
            assert y <= world.height
            left_x = random.randint(world.flags_left_min, world.flags_left_max)
            return FlagPair(world, y, left_x)

        flag_pairs: List[FlagPair] = []
        for i in range(world.flags_ammount):
            y = world.flags_start + i * world.flags_spacing_vertical
            pair = new_flag_pair(y)

            flag_pairs.append(pair)

        trees: List[Tree] = []
        def new_tree() -> Tree:
            tree = None
            while True:
                y = random.randint(0, world.height)

                min_x = max_x = world.width

                if world.is_slalom:
                    # find the pair of flags that have the tree in between
                    previous_pair_index = (y - world.flags_start) // world.flags_spacing_vertical

                    previous_pair_index = max(previous_pair_index, 0)
                    previous_pair_index = min(previous_pair_index, world.flags_ammount - 1)
                    next_pair_index = min(previous_pair_index + 1, world.flags_ammount - 1)

                    previous_pair = flag_pairs[previous_pair_index]
                    next_pair = flag_pairs[next_pair_index]

                    min_x = min(previous_pair.left_x, next_pair.left_x) - world.trees_margin_to_flags
                    max_x = max(previous_pair.right_x, next_pair.right_x) + world.trees_margin_to_flags

                distance_in_between = max_x - min_x
                x = random.randint(0, world.width - distance_in_between)

                if x > min_x: # doesn't happen in downhill mode (min_x = max_x = world.width)
                    x += distance_in_between

                tree = Tree((x, y))

                collides_with_trees = (tree.rect.colliderect(a_tree.rect) for a_tree in trees)
                if world.trees_ammount > 75:
                    collides_with_trees = None

                # should always be False, anyways
                collides_with_flags = (tree.rect.colliderect(a_flag_pair.left.rect) or tree.rect.colliderect(a_flag_pair.right.rect) for a_flag_pair in flag_pairs)

                if not (collides_with_trees and any(collides_with_trees)) and not any(collides_with_flags):
                    break # we have a good tree (it doesn't collide with anything else), we can stop trying

            return tree

        for i in range(world.trees_ammount):
            trees.append(new_tree())

        super().__init__(world, flag_pairs, trees)

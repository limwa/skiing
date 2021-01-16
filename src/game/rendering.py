
import pygame.display
from pygame import Rect, Surface

import game.assets
import game.utils
from game.camera import Camera

class Renderer:

    BACKGROUND_COLOR = (245, 245, 245)

    def __init__(self, screen: Surface):
        self.screen = screen
        self.camera = Camera(screen, 200, 150)

        self.background = Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Renderer.BACKGROUND_COLOR)

        self.header = Rect(0, 0, 800, 75)

        self.points_font = game.assets.get_font("Pixeboy", 48)
        self.time_font = game.assets.get_font("Pixeboy", 32)

    def render(self, obj):
        main_player = obj.get_main_player()

        self.screen.blit(self.background, (0, 0))
        self.camera.track(main_player.pos)

        defered_render = []
        for pair in obj.landscape.flag_pairs:
            if pair.y > main_player.pos.y:
                defered_render.append(pair)
                continue

            pair.render(self.camera)

        for tree in obj.landscape.trees:
            if tree.rect.bottom > main_player.pos.y:
                defered_render.append(tree)
                continue

            tree.render(self.camera)

        for player in obj.players:
            player.render(self.camera)

        for defered in defered_render:
            defered.render(self.camera)

        self.screen.blit(self.background, (0, 0), self.header)

        time = self.time_font.render(game.utils.format_millis(obj.game_millis), True, (0, 0, 0), Renderer.BACKGROUND_COLOR)
        time_rect = time.get_rect()

        points = self.points_font.render(str(obj.landscape.world.flags_ammount - obj.get_main_player().score), True, (0, 0, 0), Renderer.BACKGROUND_COLOR)
        points_rect = points.get_rect()

        points_rect.midbottom = self.header.center
        time_rect.midtop = self.header.center

        time_rect.move_ip(0, 10)

        self.screen.blit(time, time_rect)
        self.screen.blit(points, points_rect)

        pygame.display.flip()

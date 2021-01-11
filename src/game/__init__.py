from typing import Set
from uuid import UUID

import pygame.event
import pygame.locals
import pygame.time
import pygame.display
from pygame import Vector2, Surface, Rect

import game.utils
from game.config import WorldConfig
from game.landscape import Landscape, LocalLandscape
from game.player import Player
from game.camera import Camera
import game.assets

class Game:
    def __init__(self, screen: Surface, landscape: Landscape, *players: Player):
        self.players = list(players)
        self.landscape = landscape
        self.running = True

        self.start_millis = -1

        self.screen = screen

        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((245, 245, 245))

        self.camera = Camera(screen, 200, 150)

        self.header = Rect(0, 0, 800, 100)
        self.font = game.assets.get_font("Pixeboy", 36)

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, uuid: UUID):
        for index, player in enumerate(self.players):
            if player.uuid == uuid:
                player.keyboard.unlock()
                self.players.pop(index)
                break

    def update(self, dt):
        for player in self.players:
            prev_pos = (player.pos.x, player.pos.y)
            player.update(dt)

            for tree in self.landscape.trees:
                if tree.collides_at(prev_pos, player.pos):
                    player.velocity = Vector2(0, 0)
                    print('Collided with tree')
                    break

            for pair in self.landscape.flag_pairs:
                if pair.left.collides_at(prev_pos, player.pos) or pair.right.collides_at(prev_pos, player.pos):
                    player.velocity = Vector2(0,0)
                    print('Collided with flag')
                    
                if pair.collides_at(prev_pos, player.pos):
                    print('Scored a point!')

            if player.pos.y > self.landscape.world.height:
                self.running = False

    def render(self):
        self.screen.blit(self.background, (0, 0))

        self.camera.track(self.players[0].pos)

        for player in self.players:
            player.render(self.camera)
        
        self.landscape.render(self.camera)

        self.screen.blit(self.background, (0, 0), self.header)

        dt = game.utils.current_millis() - self.start_millis
        time = self.font.render(str(dt), True, (0, 0, 0), (245, 245, 245))
        time_rect = time.get_rect()

        time_rect.center = self.header.center

        self.screen.blit(time, time_rect)

        pygame.display.flip()

    def start(self, millis = -1):
        """ This function will block the executing environment, until the game ends. """
        self.start_millis = game.utils.current_millis() + 3000 if millis == -1 else millis

        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    return

            diff = game.utils.current_millis() - self.start_millis
            if diff >= 0:
                break

            self.render()


        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) * self.landscape.world.time_factor

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    return

                for player in self.players:
                    player.process_event(event)

            self.update(dt)
            self.render()





    # def 
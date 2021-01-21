from uuid import UUID

import pygame.event
import pygame.locals
import pygame.time
import pygame.display
from pygame import Vector2

import game.utils
from game.landscape import Landscape
from game.player import Player
from game.rendering import Renderer
import game.assets
import game.rendering

class Game:
    def __init__(self, renderer: Renderer, landscape: Landscape, *players: Player):
        self.players = list(players)
        self.landscape = landscape
        self.running = True

        self.start_millis = -1
        self.game_millis = -1

        self.renderer = renderer

        self.collision_sound = game.assets.get_sound('collision')
        self.score_sound = game.assets.get_sound('score')

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, uuid: UUID):
        for index, player in enumerate(self.players):
            if player.uuid == uuid:
                player.keyboard.unlock()
                self.players.pop(index)
                break

    def get_main_player(self):
        return self.players[0]

    def update(self, dt):
        self.game_millis = game.utils.current_millis() - self.start_millis

        for player in self.players:
            player.update(dt)

            if player.time_since_last_collision >= Player.INVULN_TIME:
                for tree in self.landscape.trees:
                    if tree.collides_at(player.collision_box):
                        player.time_since_last_collision = 0
                        player.velocity = Vector2(0, 0)
                        self.collision_sound.play()

            for pair in self.landscape.flag_pairs:
                if player.time_since_last_collision >= Player.INVULN_TIME:
                    if pair.left.collides_at(player.collision_box) or pair.right.collides_at(player.collision_box):
                        player.time_since_last_collision = 0
                        player.last_scored_pair = pair
                        player.velocity = Vector2(0,0)
                        self.collision_sound.play()

                    if player.last_scored_pair != pair:
                        if pair.collides_at(player.collision_box):
                                player.last_scored_pair = pair
                                player.score += 1
                                self.score_sound.play()

            if player.pos.y > self.landscape.world.height:
                self.running = False

    def start(self, millis = -1):
        """ This function will block the executing environment, until the game ends. """
        self.start_millis = game.utils.current_millis() + 3000 if millis == -1 else millis

        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.running = None

            self.update(0)
            self.renderer.render(self)

            if self.game_millis >= 0:
                break


        while self.running:
            dt = clock.tick(60) * self.landscape.world.time_factor

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.running = None

                for player in self.players:
                    player.process_event(event)

            self.update(dt)
            self.renderer.render(self)

        return self.running is not None

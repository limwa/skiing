from uuid import UUID

import game.utils
from game.config import WorldConfig
from game.landscape import Landscape, LocalLandscape
from game.player import Player

class Game:
    def __init__(self, landscape: Landscape, *players: Player):
        self.players = list(players)
        self.landscape = landscape

        self.start = -1

    def add_player(player: Player):
        self.player.append(player)

    def remove_player(uuid: UUID):
        for index, player in enumerate(self.players):
            if player.uuid == uuid:
                self.players.pop(index)
                break

    def start(millis = -1):
        """ This function will block the executing environment, until the game ends. """
        self.start = game.utils.current_millis() + 3000 if millis == -1 else millis

        while True:
            print("waiting")
            diff = game.utils.current_millis() - start
            if diff < 0:
                continue

            break




    # def 
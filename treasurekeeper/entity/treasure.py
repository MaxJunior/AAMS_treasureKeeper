import pygame
import os

from .entity import Entity

from ..globals import ASSETS_DIR, ChestStatus, EMPTY_BONUS


class Treasure(Entity):

    def __init__(self, pos, board):
        super().__init__(pos, board, "treasure_closed.png")
        self.gold = 10.0
        self.status = ChestStatus.CLOSED

    def remove_gold(self, amount):
        """Remove an amount of gold from the chest."""
        if self.gold - amount < 0:
            self.gold = 0
            self.status = ChestStatus.EMPTY
            sprite_fname = "treasure_empty.png"
            res = self.gold + EMPTY_BONUS
        else:
            self.gold = self.gold - amount
            self.status = ChestStatus.OPEN
            sprite_fname = "treasure_open.png"
            res = amount
        self.set_sprite(sprite_fname)
        return res

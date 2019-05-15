import pygame
import os

from .entity import Entity


class Jailcell(Entity):

    def __init__(self, pos, board):
        super().__init__(pos, board, "jailcell.png")
        self.prisoner = None

    def set_prisoner(self, hunter):
        """Changes current prisoner to Hunter hunter."""
        if self.is_occupied():
            raise Exception("Can't lock a prisoner when jailcell is occupied.")
        self.prisoner = hunter
        sprite_fname = f"jail_expl_{EXPL_COLORS[hunter.id]}.png"
        self.set_sprite(sprite_fname)

    def is_occupied(self):
        return self.prisoner is not None

    def release_prisoner(self):
        if not self.is_occupied():
            raise Exception("Can't release when there's no locked prisoner.")
        self.prisoner = None
        sprite_fname = "jailcell.png"
        self.set_sprite(sprite_fname)

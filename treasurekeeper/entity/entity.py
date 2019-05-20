import pygame
import os

from ..globals import ASSETS_DIR


class Entity:
    """Class that represents entities in Treasure Keeper."""
    def __init__(self, pos, board, sprite_fname, name):
        self.pos = pos
        self.board = board
        self.set_sprite(sprite_fname)
        self.rect = self.sprite.get_rect()
        self.name = name

    def set_sprite(self, sprite_fname):
        """Change/set the entity's sprite."""
        sprite = pygame.image.load(os.path.join(ASSETS_DIR, sprite_fname))
        self.sprite = sprite

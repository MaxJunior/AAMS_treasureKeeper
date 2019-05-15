import pygame
import os

from ..globals import ASSETS_DIR

class Entity:
    """Class that represents entities in Treasure Keeper."""
    def __init__(self, pos, board, sprite_fname):
        self.pos = pos
        self.board = board
        self.sprite = pygame.image.load(os.path.join(ASSETS_DIR, sprite_fname))
        self.rect = self.sprite.get_rect()
    
    def set_sprite(self, sprite_fname):
        sprite = pygame.image.load(os.path.join(ASSETS_DIR, sprite_fname))
        self.sprite = sprite

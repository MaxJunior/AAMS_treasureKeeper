import pygame
import os
ASSETS_DIR = "assets"
class Entity:
    """Class that represents entities in Treasure Keeper."""
    def __init__(self, pos, board, sprite_fname):
        self.pos = pos
        self.board = board
        self.sprite = pygame.image.load(os.path.join(ASSETS_DIR, sprite_fname))
        self.rect = self.sprite.get_rect()
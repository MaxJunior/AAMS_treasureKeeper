import pygame
import os


from board import Board
from entity.hunter import Hunter
# This sets the margin between each cell
MARGIN = 3

# Define some colors
BLACK = (30, 37, 48)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (213, 196, 124)
BROWN = (112, 103, 67)

GAME_TITLE = "Treasure Keeper"

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = HEIGHT = 35

class GUI:

    def __init__(self, n_cells, cell_width, cell_margin):
        self.n_cells = n_cells
        self.cell_width = cell_width
        self.cell_margin = cell_margin
        self.clock = None
        self.screen = None
        self.title = GAME_TITLE

        self.board = Board(n_cells, self)
        self.displayBoard()
        self.board.displayEntities()
        self.board.run()

    def displayBoard(self):
        grid_size = ((self.n_cells * (self.cell_width + self.cell_margin)) + self.cell_margin)
        window_size = window_size = list(grid_size for _ in range(2))

        pygame.init()
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(window_size)
        self.screen.fill(BROWN)
        for row in range(self.n_cells):
            for col in range(self.n_cells):
                x, y = self.calculate_coord(row, col)
                pygame.draw.rect(self.screen,
                                GOLD,
                                [x,
                                y,
                                self.cell_width,
                                self.cell_width])

        # Limit to 60 frames per second
        self.clock.tick(60)

        pygame.display.flip()

    def calculate_coord(self, row, col, xoffset=0):
        x = (self.cell_margin + self.cell_width) * col + self.cell_margin + xoffset
        y = (self.cell_margin + self.cell_width) * row + self.cell_margin

        return x, y

    def displayEntity(self, entity):
        row, col = entity.pos
        sprite = entity.sprite
        if isinstance(entity, Hunter):
            xoffset = 5
        else:
            xoffset = 0
        self.screen.blit(sprite, self.calculate_coord(row, col, xoffset))

        pygame.display.flip()

    def displayEntities(self):
        pass

    def removeEntity(self, entity):
        pass


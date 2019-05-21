import pygame
import os

from .board import Board
from .entity.hunter import Hunter
from .entity.treasure import Treasure

from .globals import GAME_TITLE, ASSETS_DIR, HunterStatus

# This sets the margin between each cell
MARGIN = 3

# Define some colors
BLACK = (30, 37, 48)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (213, 196, 124)
BROWN = (56, 39, 15)


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
        #self.screen.fill(BROWN)
        img = pygame.image.load(os.path.join(ASSETS_DIR, "ground.jpg"))
        
        #draw floor texture, +1 for safety
        for i in range(window_size[0] // 252 + 1):
            for j in range(window_size[1] // 253 + 1):
                self.screen.blit(img, (252*i, 253*j))

        #draw grid lines
        for i in range(self.n_cells + 1):
            hx = vy = 0
            vx = hy = i * (self.cell_margin + self.cell_width) + (self.cell_margin / 2)
            hx_end = window_size[0]
            hy_end = vx_end = hy
            vy_end = window_size[1]

            pygame.draw.line(self.screen,
                              BROWN,
                              (hx, hy),
                              (hx_end, hy_end),
                              self.cell_margin)

            pygame.draw.line(self.screen,
                              BROWN,
                              (vx, vy),
                              (vx_end, vy_end),
                              self.cell_margin)

        # Limit to 60 frames per second
        self.clock.tick(60)
        pygame.display.flip()

    def calculate_coord(self, row, col, xoffset=0, yoffset=0):
        x = (self.cell_margin + self.cell_width) * col + self.cell_margin + xoffset
        y = (self.cell_margin + self.cell_width) * row + self.cell_margin + yoffset

        return x, y

    def displayEntity(self, entity):
        row, col = entity.pos.row, entity.pos.col
        sprite = entity.sprite
        if isinstance(entity, Hunter):
            xoffset = 10
            yoffset = 3
        elif isinstance(entity, Treasure):
            xoffset = 3
            yoffset = 4
        else:
            xoffset = 0
            yoffset = 0

        self.screen.blit(sprite, self.calculate_coord(row, col, xoffset, yoffset))
        pygame.display.flip()

    def draw_fov(self, agent):
        if isinstance(agent, Hunter):
            if agent.status != HunterStatus.ALIVE:
                return
        fov = agent.look_fov(3)
        color = agent.get_color() if isinstance(agent, Hunter) else "orange"
        for pos in fov:
            coord = self.calculate_coord(pos.row, pos.col)
            if color == "red":
                color = RED
            elif color == "blue":
                color = BLUE
            elif color == "green":
                color = GREEN
            elif color == "yellow":
                color = YELLOW
            pygame.draw.rect(self.screen, color, [coord[0], coord[1],
                             self.cell_width, self.cell_width])
        pygame.display.flip()

    def displayEntities(self):
        pass

    def removeEntity(self, entity):
        pass

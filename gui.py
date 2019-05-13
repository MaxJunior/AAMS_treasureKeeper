import pygame

# This sets the margin between each cell
MARGIN = 3

# Define some colors
BLACK = (30, 37, 48)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (216, 179, 78)

GAME_TITLE = "Treasure Keeper"

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = HEIGHT = 35

class GUI:

    def __init__(self, n_cells, cell_width, cell_margin, board):
        self.n_cells = n_cells
        self.cell_width = cell_width
        self.cell_margin = cell_margin
        self.board = board
        self.clock = None
        self.screen = None
        self.title = GAME_TITLE

    def displayBoard(self):
        grid_size = ((self.n_cells * (WIDTH + MARGIN)) + MARGIN)
        window_size = window_size = list(grid_size for _ in range(2))

        pygame.init()
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(window_size)
        self.screen.fill(BLACK)
        for row in range(self.n_cells):
            for column in range(self.n_cells):
                pygame.draw.rect(self.screen,
                                WHITE,
                                [(self.cell_margin + self.cell_width) * column + self.cell_margin,
                                (self.cell_margin + self.cell_width) * row + self.cell_margin,
                                self.cell_width,
                                self.cell_width])

        # Limit to 60 frames per second
        self.clock.tick(60)

        pygame.display.flip()

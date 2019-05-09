"""
COURSE  : AAMS
GROUP N : 48
76213   : Goncalo Lopes
79457   : Maxwell Junior
"""

from typing import List, Tuple
from tk_types import Content, Pos, Group, Move, Adj
import pygame

WINDOW_RIGHT_MARGIN = 200
GRID_DIMS = (12, 12)

# Define some colors
BLACK = (30, 37, 48)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (216, 179, 78)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = HEIGHT = 35

# This sets the margin between each cell
MARGIN = 3
grid_size = ((GRID_DIMS[0] * (WIDTH + MARGIN)) + MARGIN)
window_size = list(grid_size for _ in range(2))

window_size[0] += WINDOW_RIGHT_MARGIN
screen = pygame.display.set_mode(window_size)
done = False

pygame.init()
pygame.display.set_caption("Treasure Keeper")
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(GRID_DIMS[0]):
        for column in range(GRID_DIMS[1]):
            color = WHITE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    # Draw side panel
    pygame.draw.rect(screen,
                     GOLD,
                     [grid_size,
                      0,
                      WINDOW_RIGHT_MARGIN,
                      grid_size])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()

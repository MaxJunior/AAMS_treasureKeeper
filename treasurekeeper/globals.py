import os
from enum import Enum


class HunterStatus(Enum):
    DEAD = 0
    ALIVE = 1
    LOCKED = 2
    GRABBED = 3

class ChestStatus(Enum):
    CLOSED = 0
    OPEN = 1
    EMPTY = 2

ASSETS_DIR = os.path.join(os.getcwd(), "treasurekeeper", "assets")
GAME_TITLE = "Treasure Keeper"

EXPL_COLORS = ["blue", "green", "red", "yellow"]
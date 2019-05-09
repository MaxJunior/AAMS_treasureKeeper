from enum import Enum


class HunterStatus(Enum):
    DEAD = 0
    ALIVE = 1
    LOCKED = 2
    GRABBED = 3

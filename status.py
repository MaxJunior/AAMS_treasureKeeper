from enum import Enum


class Status(Enum):
    DEAD = 0
    ALIVE = 1
    LOCKED = 2
    GRABBED = 3

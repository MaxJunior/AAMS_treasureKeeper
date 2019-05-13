from .entity import Entity

class Treasure(Entity):

    def __init__(self, pos, board):
        super().__init__(pos, board, "treasure_closed.png")
        self.gold = 10.0

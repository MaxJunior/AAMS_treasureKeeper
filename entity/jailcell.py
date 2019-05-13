from .entity import Entity

class Jailcell(Entity):

    def __init__(self, pos, board):
        super().__init__(pos, board, "jailcell.png")
        self.prisoner = None

from tk_types import Pos, Move


def make_move(p_initial: Pos, p_final: Pos) -> Move :
    """Create a move"""
    return [p_initial, p_final]

def move_initial (move: Move) -> Pos:
    """Returns the initial position"""
    return move[0]

def move_final(move: Move) -> Pos:
    """Returns the final position"""
    return move[1]
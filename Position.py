from TK_Types import Pos


#_____________________________________________________________
# TAI pos

def make_pos (line: int, colune: int) -> Pos:
    """Creates a position."""
    return (line, colune)

def pos_l (pos: Pos) -> int:
    """Returns the line of the 'pos' position."""
    return pos[0]

def pos_c (pos: Pos) -> int:
    """Returns the column of the 'pos' position."""
    return pos[1]

def pos_sum(pos1: Pos, pos2: Pos) -> Pos:
    """Returns the sum of two positions."""
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


from typing import Tuple, List
from entity.entity import Entity
#________________________________________________________
# Types Annotations

Content = Entity
Pos = Tuple[int, int]
Board_Type = List[List[Content]]
Group = List[Pos]
Move = List[Pos]
Adj = List[Pos]

#________________________________________________________

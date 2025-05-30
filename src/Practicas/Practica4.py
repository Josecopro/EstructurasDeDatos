from dataclasses import dataclass, field
from abc import abstractmethod, ABC

@dataclass
class Player:
    pass

@dataclass
class Space:
    pass

@dataclass
class SpaceItems(ABC):
    @abstractmethod
    def Idk():
        pass

@dataclass
class Walls(SpaceItems):
    def __init__(self):
        self._items = []

    def Idk():
        pass

@dataclass
class Traps(SpaceItems):
    def __init__(self):
        pass

    def Idk():
        pass
        
@dataclass 
class Retarder(SpaceItems):
    def __init__(self):
        pass

    def Idk():
        pass
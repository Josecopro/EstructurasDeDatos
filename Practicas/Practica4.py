from dataclasses import dataclass, field
from abc import abstractmethod, ABC
import random

class PriorityQueue:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)
        self.data.sort(key=lambda x: x[0])

    def pop(self):
        if self.data:
            return self.data.pop(0)
        else:
            print("Ta vacio papi, paila")

    def __len__(self):
        return len(self.data)

@dataclass
class Player:
    Name : str = "🤸"
    Position: list[int] = field(default_factory = list)
    IsRetard: bool = False
    IsDumb: bool = False
    IsFinished: bool = False

    def Move(self, Movement):
        if not self.IsDumb and not self.IsFinished and not self.IsRetard:
            pass


@dataclass
class SpaceItems(ABC):
    Name: str
    Position: list[int] = field(default_factory=list)


    @abstractmethod
    def Idk():
        pass

@dataclass
class FinishLine(SpaceItems):
    Name: str = "🏁"

    def Idk():
        pass

@dataclass
class Walls(SpaceItems):
    Name: str =  "🧱"

    def Idk():
        pass

@dataclass
class Traps(SpaceItems):
    Name: str = "🪤"
    def Idk():
        pass
        
@dataclass 
class Retarder(SpaceItems):
    Name: str = "🍌"

    def Idk():
        pass


@dataclass
class Space:
    GridSize: int
    FinishLine: FinishLine
    NumberOfPlayers: int
    NumberOfWalls: int
    Trash: int
    Grid: list[list] = field(default_factory=list)
    PlayerList: list[Player] = field(default_factory=list)
    Iteration: int = 0 

    def StartSim(self):
        self.Grid = [[None for _ in range(self.GridSize)] for _ in range(self.GridSize)]
        self.Grid[self.FinishLine.Position[0]][self.FinishLine.Position[1]] = self.FinishLine
        self.CreatePlayers()
        for Player in self.PlayerList:
            self.Grid[Player.Position[0]][Player.Position[1]] = Player
        for wall in self.CreateWalls():
            self.Grid[wall.Position[0]][wall.Position[1]] = wall
        
        for trash in self.CreateTrash():
            self.Grid[trash.Position[0]][trash.Position[1]] = trash


    def UpdateFinishLine(self, NewPos:list[int]):
        self.FinishLine.Position = NewPos


    def UpdateSim(self):
        self.AddWall([random.randint(0,self.GridSize -1 ), random.randint(0, self.GridSize - 1)])

    def ShowGrid(self):
        if self.Iteration == 0:
            self.StartSim()
        else:
            self.UpdateSim()
        for row in self.Grid:
            print(" ".join(cell.Name if cell else "⬜" for cell in row))

    def CreatePlayers(self):
        for _ in range(self.NumberOfPlayers):
            self.PlayerList.append(Player(Position=[random.randint(0, self.GridSize-1), random.randint(0, self.GridSize-1)]))

    def CreateWalls(self) -> list[Walls]:
        WallsList: list = []
        for _ in range(self.NumberOfWalls):
                pos = [random.randint(0, self.GridSize-1), random.randint(0, self.GridSize-1)]
                if (pos != self.FinishLine.Position and all(player.Position != pos for player in self.PlayerList)):
                    WallsList.append ( Walls(Position=pos))
        return WallsList

    def CreateTrash(self) -> list[Traps | Retarder]:
        TrashList: list = []
        PosibleItem: list = [Traps, Retarder]
        for _ in range(self.Trash):
                pos = [random.randint(0, self.GridSize-1), random.randint(0, self.GridSize-1)]
                if (pos != self.FinishLine.Position and all(player.Position != pos for player in self.PlayerList)):
                    RandomItem = random.choice(PosibleItem)
                    TrashList.append ( RandomItem(Position=pos))
        return TrashList
    
    def AddWall(self, WallPos:list[int]):
        if (WallPos != self.FinishLine.Position and all(player.Position != WallPos for player in self.PlayerList)):
            wall = Walls(Position=WallPos)
            self.Grid[wall.Position[0]][wall.Position[1]] = wall
        else:
            print("No se puede ubicar el bloqueo, ya existe un elemento alli")




    def MovePlayers(self):
        for player in self.PlayerList:
            a = self.CalculateBestRoute(player.Position)
            print(a)


    def CalculateBestRoute(self, ActualPos:list[int]):
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        visited = set()
        pq = PriorityQueue()
        pq.push((0, ActualPos, [ActualPos]))
        finish = self.FinishLine.Position

        while len(pq) > 0:
            cost, pos, path = pq.pop()
            pos_tuple = tuple(pos)
            if pos_tuple in visited:
                continue
            visited.add(pos_tuple)

            if pos == finish:
                return path  # Camino encontrado

            for dx, dy in directions:
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < self.GridSize and 0 <= ny < self.GridSize:
                    cell = self.Grid[nx][ny]
                    # No visitar muros
                    if cell is None or isinstance(cell, FinishLine):
                        if (nx, ny) not in visited:
                            pq.push((cost+1, [nx, ny], path + [[nx, ny]]))
        return f"Ay muchachos"
    



espacio = Space(10, FinishLine(Position=[7,7]), 2, 15, 5)

espacio.ShowGrid()

espacio.MovePlayers()
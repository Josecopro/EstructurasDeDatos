from abc import ABC, abstractmethod
import random

#basura 1
class Organismo(ABC):
    def __init__(self, x, y, nombre):
        self.x = x
        self.y = y
        self.nombre = nombre

    def mover(self, grid, n):
        return (self.x, self.y)

    @abstractmethod
    def __repr__(self):
        pass

class Depredador(Organismo):
    def __init__(self, x, y, hambre=0, nombre="D"):
        super().__init__(x, y, nombre)
        self.hambre = hambre

    def mover(self, grid, n):
        move = self.buscar_presa_visible(grid, n)
        if move is not None:
            return move
        moves = self.get_adjacent_positions(n)
        move = self.buscar_presa_recursivo(moves, grid, 0)
        if move is None:
            empty_moves = self.filtrar_movimientos_vacios(moves, grid, 0, [])
            if empty_moves:
                move = random.choice(empty_moves)
            else:
                move = (self.x, self.y)
        return move

    def buscar_presa_visible(self, grid, n):
        candidatos = []
        for j in range(n):
            if j != self.y:
                org = grid[self.x][j]
                if org is not None and isinstance(org, Presa):
                    candidatos.append(('fila', self.x, j, abs(j - self.y)))
        for i in range(n):
            if i != self.x:
                org = grid[i][self.y]
                if org is not None and isinstance(org, Presa):
                    candidatos.append(('col', i, self.y, abs(i - self.x)))
        if candidatos:
            candidato = min(candidatos, key=lambda x: x[3])
            if candidato[0] == 'fila':
                if candidato[2] > self.y:
                    return (self.x, self.y + 1)
                else:
                    return (self.x, self.y - 1)
            else:
                if candidato[1] > self.x:
                    return (self.x + 1, self.y)
                else:
                    return (self.x - 1, self.y)
        return None

    def buscar_presa_recursivo(self, moves, grid, idx):
        if idx >= len(moves):
            return None
        x, y = moves[idx]
        org = grid[x][y]
        if org is not None and isinstance(org, Presa):
            return (x, y)
        return self.buscar_presa_recursivo(moves, grid, idx + 1)

    def filtrar_movimientos_vacios(self, moves, grid, idx, result):
        if idx >= len(moves):
            return result
        x, y = moves[idx]
        if grid[x][y] is None:
            result.append((x, y))
        return self.filtrar_movimientos_vacios(moves, grid, idx + 1, result)

    def get_adjacent_positions(self, n):
        moves = []
        if self.x - 1 >= 0:
            moves.append((self.x - 1, self.y))
        if self.x + 1 < n:
            moves.append((self.x + 1, self.y))
        if self.y - 1 >= 0:
            moves.append((self.x, self.y - 1))
        if self.y + 1 < n:
            moves.append((self.x, self.y + 1))
        return moves

    def __repr__(self):
        return self.nombre

class Presa(Organismo):
    def __init__(self, x, y, nombre="P"):
        super().__init__(x, y, nombre)

    def mover(self, grid, n):
        moves = self.get_adjacent_positions(n)
        empty_moves = self.filtrar_movimientos_vacios(moves, grid, 0, [])
        if empty_moves:
            return random.choice(empty_moves)
        return (self.x, self.y)

    def get_adjacent_positions(self, n):
        moves = []
        if self.x - 1 >= 0:
            moves.append((self.x - 1, self.y))
        if self.x + 1 < n:
            moves.append((self.x + 1, self.y))
        if self.y - 1 >= 0:
            moves.append((self.x, self.y - 1))
        if self.y + 1 < n:
            moves.append((self.x, self.y + 1))
        return moves

    def filtrar_movimientos_vacios(self, moves, grid, idx, result):
        if idx >= len(moves):
            return result
        x, y = moves[idx]
        if grid[x][y] is None or isinstance(grid[x][y], Planta):
            result.append((x, y))
        return self.filtrar_movimientos_vacios(moves, grid, idx + 1, result)

    def __repr__(self):
        return self.nombre

class Planta(Organismo):
    def __init__(self, x, y, nombre="*"):
        super().__init__(x, y, nombre)

    def mover(self, grid, n):
        return (self.x, self.y)

    def __repr__(self):
        return self.nombre

#basura 2 
class Ecosistema:
    def __init__(self, n, organismos):
        self.n = n
        self.grid = self.crear_grid(n)
        self.inicializar_ecosistema(organismos)
        self.ciclo = 0

    def crear_fila(self, n, col=0, fila=None):
        if fila is None:
            fila = []
        if col >= n:
            return fila
        fila.append(None)
        return self.crear_fila(n, col + 1, fila)

    def crear_grid(self, n, row=0, grid=None):
        if grid is None:
            grid = []
        if row >= n:
            return grid
        grid.append(self.crear_fila(n))
        return self.crear_grid(n, row + 1, grid)

    def inicializar_ecosistema(self, organismos, idx=0):
        if idx >= len(organismos):
            return
        self.agregar_organismo(organismos[idx])
        self.inicializar_ecosistema(organismos, idx + 1)

    def imprimir_ecosistema(self, row=0, col=0, output=""):
        if row >= self.n:
            print(output)
            return
        if col >= self.n:
            output += "\n"
            self.imprimir_ecosistema(row + 1, 0, output)
            return
        organism = self.grid[row][col]
        output += repr(organism) if organism is not None else "."
        self.imprimir_ecosistema(row, col + 1, output)

    def actualizar_ecosistema(self, row=0, col=0):
        if row >= self.n:
            return
        if col >= self.n:
            self.actualizar_ecosistema(row + 1, 0)
            return
        organism = self.grid[row][col]
        if organism is not None and not hasattr(organism, 'actualizado'):
            organism.actualizado = True
            new_pos = organism.mover(self.grid, self.n)
            if new_pos != (row, col):
                self.grid[row][col] = None
                dest_org = self.grid[new_pos[0]][new_pos[1]]
                if dest_org is not None:
                    if isinstance(organism, Depredador) and isinstance(dest_org, Presa):
                        self.grid[new_pos[0]][new_pos[1]] = organism
                        organism.x, organism.y = new_pos
                    elif isinstance(organism, Presa) and isinstance(dest_org, Planta):
                        self.grid[new_pos[0]][new_pos[1]] = organism
                        organism.x, organism.y = new_pos
                    else:
                        self.grid[row][col] = organism
                else:
                    self.grid[new_pos[0]][new_pos[1]] = organism
                    organism.x, organism.y = new_pos
        self.actualizar_ecosistema(row, col + 1)

    def reset_actualizados(self, row=0, col=0):
        if row >= self.n:
            return
        if col >= self.n:
            self.reset_actualizados(row + 1, 0)
            return
        if self.grid[row][col] is not None and hasattr(self.grid[row][col], 'actualizado'):
            del self.grid[row][col].actualizado
        self.reset_actualizados(row, col + 1)

    def get_state(self):
        state = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] is not None:
                    state.append((i, j, self.grid[i][j].nombre))
        return sorted(state)

    def interacciones_posibles(self):
        count_depredador = 0
        count_presa = 0
        count_planta = 0
        for i in range(self.n):
            for j in range(self.n):
                org = self.grid[i][j]
                if org is not None:
                    if isinstance(org, Depredador):
                        count_depredador += 1
                    elif isinstance(org, Presa):
                        count_presa += 1
                    elif isinstance(org, Planta):
                        count_planta += 1
        return (count_depredador > 0 and count_presa > 0) or (count_presa > 0 and count_planta > 0)

    def agregar_organismo(self, organismo):
        empty_cells = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] is None:
                    empty_cells.append((i, j))
        if empty_cells:
            pos = random.choice(empty_cells)
            organismo.x, organismo.y = pos
            self.grid[pos[0]][pos[1]] = organismo

#simulacion 

organismos_iniciales = [
    Depredador(0, 0, nombre="D"),
    Presa(0, 0, nombre="P"),
    Planta(0, 0, nombre="*")
]

n = 5
ecosistema = Ecosistema(n, organismos_iniciales)
prev_state = ecosistema.get_state()

while True:
    if not ecosistema.interacciones_posibles():
        break

    print(f"Ciclo {ecosistema.ciclo}:")
    ecosistema.imprimir_ecosistema()
    ecosistema.actualizar_ecosistema()
    ecosistema.reset_actualizados()

    if ecosistema.ciclo != 0 and ecosistema.ciclo % 3 == 0:
        if random.choice([True, False]):
            ecosistema.agregar_organismo(Depredador(0, 0, nombre="D"))
        else:
            ecosistema.agregar_organismo(Presa(0, 0, nombre="P"))

    if ecosistema.ciclo != 0 and ecosistema.ciclo % 4 == 0:
        ecosistema.agregar_organismo(Planta(0, 0, nombre="*"))
        ecosistema.agregar_organismo(Planta(0, 0, nombre="*"))

    new_state = ecosistema.get_state()
    if new_state == prev_state:
        break
    prev_state = new_state
    ecosistema.ciclo += 1

print("Simulación terminada: no hay más movimientos posibles.")
print("Estado final del ecosistema:")
ecosistema.imprimir_ecosistema()

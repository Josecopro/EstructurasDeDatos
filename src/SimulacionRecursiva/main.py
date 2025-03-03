import random
import math

# Clase base para los organismos
class Organismo:
    def __init__(self, x, y, energia):
        self.x = x
        self.y = y
        self.energia = energia

    def esta_vivo(self):
        return self.energia > 0

    def morir(self):
        self.energia = 0

# Clase para los depredadores
class Depredador(Organismo):
    def __init__(self, x, y, energia):
        super().__init__(x, y, energia)

    def cazar(self, presa):
        self.energia += presa.energia
        presa.morir()

    def perder_energia(self):
        self.energia -= 1  # Pérdida de energía por ciclo

# Clase para las presas
class Presa(Organismo):
    def __init__(self, x, y, energia):
        super().__init__(x, y, energia)

    def comer(self, planta):
        self.energia += planta.energia
        planta.morir()

    def perder_energia(self):
        self.energia -= 1  # Pérdida de energía por ciclo

# Clase para las plantas
class Planta(Organismo):
    def __init__(self, x, y, energia):
        super().__init__(x, y, energia)

    def regenerar(self):
        self.energia = 10  # Valor de regeneración

# Clase para el ecosistema
class Ecosistema:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.matriz = [[None for _ in range(tamaño)] for _ in range(tamaño)]
        self.ciclos = 0

    def agregar_organismo(self, organismo):
        if 0 <= organismo.x < self.tamaño and 0 <= organismo.y < self.tamaño:
            if self.matriz[organismo.x][organismo.y] is None:
                self.matriz[organismo.x][organismo.y] = organismo
            else:
                # Si la celda está ocupada, buscar una celda vacía cercana
                self.mover_a_celda_vacia(organismo)
        else:
            raise ValueError(f"Coordenadas ({organismo.x}, {organismo.y}) fuera de los límites de la matriz.")

    def mover_a_celda_vacia(self, organismo):
        # Buscar una celda vacía cercana usando recursividad
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
        self.buscar_celda_vacia_recursivo(organismo, direcciones, 0)

    def buscar_celda_vacia_recursivo(self, organismo, direcciones, indice):
        if indice >= len(direcciones):
            return None # No hay celdas vacías cercanas

        dx, dy = direcciones[indice]
        nueva_x, nueva_y = organismo.x + dx, organismo.y + dy

        if 0 <= nueva_x < self.tamaño and 0 <= nueva_y < self.tamaño:
            if self.matriz[nueva_x][nueva_y] is None:
                self.matriz[nueva_x][nueva_y] = organismo
                organismo.x, organismo.y = nueva_x, nueva_y
                return

        self.buscar_celda_vacia_recursivo(organismo, direcciones, indice + 1)

    def actualizar(self):
        self.ciclos += 1
        self.actualizar_recursivo(0, 0)
        self.regenerar_plantas_recursivo(0, 0)

        # Cada 3 ciclos, agregar un nuevo depredador y una nueva presa
        if self.ciclos % 3 == 0 and self.ciclos != 0:  # Asegurar que no se agregue en el ciclo 0
            self.agregar_nuevo_depredador()
            self.agregar_nueva_presa()

    def agregar_nuevo_depredador(self):
        x, y = self.encontrar_celda_vacia()
        if x is not None and y is not None:
            nuevo_depredador = Depredador(x, y, 10)
            self.agregar_organismo(nuevo_depredador)

    def agregar_nueva_presa(self):
        x, y = self.encontrar_celda_vacia()
        if x is not None and y is not None:
            nueva_presa = Presa(x, y, 5)
            self.agregar_organismo(nueva_presa)

    def encontrar_celda_vacia(self):
        # Buscar una celda vacía usando recursividad
        celdas_vacias = self.obtener_celdas_vacias_recursivo(0, 0, [])
        if celdas_vacias:
            return random.choice(celdas_vacias)
        return None, None

    def obtener_celdas_vacias_recursivo(self, i, j, celdas_vacias):
        if i >= self.tamaño:
            return celdas_vacias
        if j >= self.tamaño:
            return self.obtener_celdas_vacias_recursivo(i + 1, 0, celdas_vacias)

        if self.matriz[i][j] is None:
            celdas_vacias.append((i, j))

        return self.obtener_celdas_vacias_recursivo(i, j + 1, celdas_vacias)

    def actualizar_recursivo(self, i, j):
        if i >= self.tamaño:
            return
        if j >= self.tamaño:
            self.actualizar_recursivo(i + 1, 0)
            return

        organismo = self.matriz[i][j]
        if organismo and organismo.esta_vivo():
            if isinstance(organismo, Depredador):
                organismo.perder_energia()  # Depredador pierde energía
                if not organismo.esta_vivo():
                    self.matriz[i][j] = None  # Eliminar depredador si muere
                else:
                    self.mover_depredador(organismo)
                    self.evaluar_caza_recursivo(organismo, i, j, 0)
            elif isinstance(organismo, Presa):
                organismo.perder_energia()  # Presa pierde energía
                if not organismo.esta_vivo():
                    self.matriz[i][j] = None  # Eliminar presa si muere
                else:
                    self.mover_presa(organismo)
                    self.evaluar_comida_recursivo(organismo, i, j, 0)

        self.actualizar_recursivo(i, j + 1)

    def mover_depredador(self, depredador):
        # Buscar la presa más cercana
        presa = self.buscar_presa_mas_cercana_recursivo(depredador, 0, 0, None, float('inf'))
        if presa:
            self.mover_hacia(depredador, presa.x, presa.y)
        else:
            self.mover_aleatorio(depredador)

    def buscar_presa_mas_cercana_recursivo(self, depredador, i, j, presa_mas_cercana, distancia_minima):
        if i >= self.tamaño:
            return presa_mas_cercana
        if j >= self.tamaño:
            return self.buscar_presa_mas_cercana_recursivo(depredador, i + 1, 0, presa_mas_cercana, distancia_minima)

        organismo = self.matriz[i][j]
        if isinstance(organismo, Presa) and organismo.esta_vivo():
            distancia = math.sqrt((depredador.x - i) ** 2 + (depredador.y - j) ** 2)
            if distancia < distancia_minima:
                presa_mas_cercana = organismo
                distancia_minima = distancia

        return self.buscar_presa_mas_cercana_recursivo(depredador, i, j + 1, presa_mas_cercana, distancia_minima)

    def mover_presa(self, presa):
        # Buscar la planta más cercana
        planta = self.buscar_planta_mas_cercana_recursivo(presa, 0, 0, None, float('inf'))
        if planta:
            self.mover_hacia(presa, planta.x, planta.y)
        else:
            self.mover_aleatorio(presa)

    def buscar_planta_mas_cercana_recursivo(self, presa, i, j, planta_mas_cercana, distancia_minima):
        if i >= self.tamaño:
            return planta_mas_cercana
        if j >= self.tamaño:
            return self.buscar_planta_mas_cercana_recursivo(presa, i + 1, 0, planta_mas_cercana, distancia_minima)

        organismo = self.matriz[i][j]
        if isinstance(organismo, Planta) and organismo.esta_vivo():
            distancia = math.sqrt((presa.x - i) ** 2 + (presa.y - j) ** 2)
            if distancia < distancia_minima:
                planta_mas_cercana = organismo
                distancia_minima = distancia

        return self.buscar_planta_mas_cercana_recursivo(presa, i, j + 1, planta_mas_cercana, distancia_minima)

    def mover_hacia(self, organismo, x_destino, y_destino):
        # Mover hacia la celda de destino
        if x_destino > organismo.x:
            organismo.x += 1
        elif x_destino < organismo.x:
            organismo.x -= 1
        elif y_destino > organismo.y:
            organismo.y += 1
        elif y_destino < organismo.y:
            organismo.y -= 1

        # Actualizar la matriz
        self.matriz[organismo.x][organismo.y] = organismo
        self.matriz[x_destino][y_destino] = None

    def mover_aleatorio(self, organismo):
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
        dx, dy = random.choice(direcciones)
        nueva_x, nueva_y = organismo.x + dx, organismo.y + dy

        if 0 <= nueva_x < self.tamaño and 0 <= nueva_y < self.tamaño:
            if self.matriz[nueva_x][nueva_y] is None:
                self.matriz[organismo.x][organismo.y] = None
                self.matriz[nueva_x][nueva_y] = organismo
                organismo.x, organismo.y = nueva_x, nueva_y

    def evaluar_caza_recursivo(self, depredador, x, y, indice):
        if indice >= 4:
            return

        dx, dy = [(-1, 0), (1, 0), (0, -1), (0, 1)][indice]
        nueva_x, nueva_y = x + dx, y + dy

        if 0 <= nueva_x < self.tamaño and 0 <= nueva_y < self.tamaño:
            organismo = self.matriz[nueva_x][nueva_y]
            if isinstance(organismo, Presa) and organismo.esta_vivo():
                depredador.cazar(organismo)
                self.matriz[nueva_x][nueva_y] = None
                return

        self.evaluar_caza_recursivo(depredador, x, y, indice + 1)

    def evaluar_comida_recursivo(self, presa, x, y, indice):
        if indice >= 4:
            return

        dx, dy = [(-1, 0), (1, 0), (0, -1), (0, 1)][indice]
        nueva_x, nueva_y = x + dx, y + dy

        if 0 <= nueva_x < self.tamaño and 0 <= nueva_y < self.tamaño:
            organismo = self.matriz[nueva_x][nueva_y]
            if isinstance(organismo, Planta) and organismo.esta_vivo():
                presa.comer(organismo)
                self.matriz[nueva_x][nueva_y] = None
                return

        self.evaluar_comida_recursivo(presa, x, y, indice + 1)

    def regenerar_plantas_recursivo(self, i, j):
        if i >= self.tamaño:
            return
        if j >= self.tamaño:
            self.regenerar_plantas_recursivo(i + 1, 0)
            return

        if self.matriz[i][j] is None and self.ciclos % 5 == 0:
            self.matriz[i][j] = Planta(i, j, 10)  # Regenerar planta

        self.regenerar_plantas_recursivo(i, j + 1)

    def hay_comida_para_depredadores(self):
        # Verificar si hay presas vivas usando recursividad
        return self.hay_comida_para_depredadores_recursivo(0, 0)

    def hay_comida_para_depredadores_recursivo(self, i, j):
        if i >= self.tamaño:
            return False
        if j >= self.tamaño:
            return self.hay_comida_para_depredadores_recursivo(i + 1, 0)

        organismo = self.matriz[i][j]
        if isinstance(organismo, Presa) and organismo.esta_vivo():
            return True

        return self.hay_comida_para_depredadores_recursivo(i, j + 1)

    def hay_comida_para_presas(self):
        # Verificar si hay plantas vivas usando recursividad
        return self.hay_comida_para_presas_recursivo(0, 0)

    def hay_comida_para_presas_recursivo(self, i, j):
        if i >= self.tamaño:
            return False
        if j >= self.tamaño:
            return self.hay_comida_para_presas_recursivo(i + 1, 0)

        organismo = self.matriz[i][j]
        if isinstance(organismo, Planta) and organismo.esta_vivo():
            return True

        return self.hay_comida_para_presas_recursivo(i, j + 1)

    def mostrar_ecosistema_recursivo(self, i, j):
        if i >= self.tamaño:
            print()
            return
        if j >= self.tamaño:
            print()
            self.mostrar_ecosistema_recursivo(i + 1, 0)
            return

        organismo = self.matriz[i][j]
        if isinstance(organismo, Depredador):
            print("🐺", end=" ")  # Emoji para depredador
        elif isinstance(organismo, Presa):
            print("🐇", end=" ")  # Emoji para presa
        elif isinstance(organismo, Planta):
            print("🌱", end=" ")  # Emoji para planta
        else:
            print(".", end=" ")  # Celda vacía

        self.mostrar_ecosistema_recursivo(i, j + 1)
    
    def whatis(self):
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                print(f"({i}, {j}): {self.matriz[i][j]}")

# Crear un ecosistema de 5x5
ecosistema = Ecosistema(5)

# Agregar 5 presas, 1 depredador y 3 plantas al inicio
for _ in range(5):
    x, y = ecosistema.encontrar_celda_vacia()
    if x is not None and y is not None:
        nueva_presa = Presa(x, y, 5)
        ecosistema.agregar_organismo(nueva_presa)

x, y = ecosistema.encontrar_celda_vacia()
if x is not None and y is not None:
    depredador = Depredador(x, y, 10)
    ecosistema.agregar_organismo(depredador)

for _ in range(3):
    x, y = ecosistema.encontrar_celda_vacia()
    if x is not None and y is not None:
        planta = Planta(x, y, 10)
        ecosistema.agregar_organismo(planta)

# Simular hasta que no haya comida para depredadores o presas
print("Estado inicial del ecosistema:")
ecosistema.mostrar_ecosistema_recursivo(0, 0)

while ecosistema.hay_comida_para_depredadores() or ecosistema.hay_comida_para_presas():
    print(f"Ciclo {ecosistema.ciclos + 1}:")
    ecosistema.actualizar()
    ecosistema.mostrar_ecosistema_recursivo(0, 0)

print("Simulación terminada.")

#whatis
ecosistema.whatis()

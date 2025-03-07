import random
import time
import copy

random.seed(42)


class Depredador:
    def __init__(self, barra_energia=5, barra_alimento=3):
        self.barra_energia = barra_energia
        self.barra_alimento = barra_alimento
        self.movido = False

    def __repr__(self):
        return "W"  # Lobo (Depredador)


class Presa:
    def __init__(self, barra_energia=3):
        self.barra_energia = barra_energia
        self.movido = False

    def __repr__(self):
        return "R"  # Conejo (Presa)


class Planta:
    def __init__(self):
        self.movido = False  # para uniformidad

    def __repr__(self):
        return "*"


# Función recursiva para imprimir la matriz
def imprimir_matriz(matriz, indice_fila=0):
    if indice_fila >= len(matriz):
        print()
        return

    print(
        " ".join(
            [
                str(elemento) if elemento is not None else "."
                for elemento in matriz[indice_fila]
            ]
        )
    )
    imprimir_matriz(matriz, indice_fila + 1)


# Función recursiva para obtener las posiciones adyacentes válidas (arriba, abajo, izquierda, derecha)
def obtener_posiciones_adyacentes(
    matriz, indice_fila, indice_columna, direcciones=None
):
    if direcciones is None:
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if len(direcciones) == 0:
        return []
    else:
        (cambio_fila, cambio_columna) = direcciones[0]
        nueva_fila = indice_fila + cambio_fila
        nueva_columna = indice_columna + cambio_columna
        direcciones.pop(0)
        movimientos_posibles = obtener_posiciones_adyacentes(
            matriz, indice_fila, indice_columna, direcciones
        )
        if 0 <= nueva_fila < len(matriz) and 0 <= nueva_columna < len(matriz):
            return [(nueva_fila, nueva_columna)] + movimientos_posibles
        else:
            return movimientos_posibles


# Función recursiva para filtrar posiciones vacías de una lista de posiciones
def filtrar_posiciones_vacias(matriz, lista_posiciones, indice=0, acumulador=None):
    if acumulador is None:
        acumulador = []
    if indice >= len(lista_posiciones):
        return acumulador
    else:
        (fila, columna) = lista_posiciones[indice]
        if matriz[fila][columna] is None:
            acumulador.append((fila, columna))
        return filtrar_posiciones_vacias(
            matriz, lista_posiciones, indice + 1, acumulador
        )


# Función recursiva para buscar en una dirección (cambio_fila, cambio_columna) la primera presa visible (en la misma fila o columna)
def buscar_en_direccion(
    matriz, fila, columna, cambio_fila, cambio_columna, distancia=1
):
    nueva_fila = fila + cambio_fila
    nueva_columna = columna + cambio_columna
    if (
        nueva_fila < 0
        or nueva_fila >= len(matriz)
        or nueva_columna < 0
        or nueva_columna >= len(matriz)
    ):
        return None
    celda = matriz[nueva_fila][nueva_columna]
    if isinstance(celda, Presa):
        return (nueva_fila, nueva_columna, distancia)
    else:
        return buscar_en_direccion(
            matriz,
            nueva_fila,
            nueva_columna,
            cambio_fila,
            cambio_columna,
            distancia + 1,
        )


# Función recursiva para obtener la presa visible más cercana (en las 4 direcciones)
def obtener_presa_visible(matriz, fila, columna, direcciones=None, acumulador=None):
    if direcciones is None:
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if acumulador is None:
        acumulador = []
    if not direcciones:
        if not acumulador:
            return None
        mejor = acumulador[0]

        def seleccionar_mejor(lista, indice, actual):
            if indice >= len(lista):
                return actual
            candidato = lista[indice]
            if candidato[2] < actual[2]:
                actual = candidato
            return seleccionar_mejor(lista, indice + 1, actual)

        return seleccionar_mejor(acumulador, 1, mejor)
    else:
        (cambio_fila, cambio_columna) = direcciones[0]
        resultado = buscar_en_direccion(
            matriz, fila, columna, cambio_fila, cambio_columna
        )
        if resultado is not None:
            acumulador.append(resultado)
        return obtener_presa_visible(matriz, fila, columna, direcciones[1:], acumulador)


# Función que devuelve el signo de un número
def signo(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# Función recursiva para intentar reproducir un organismo en celdas adyacentes vacías
def intentar_reproducir(
    matriz,
    fila,
    columna,
    organismo,
    umbral,
    constructor_descendiente,
    posiciones_adyacentes=None,
):
    if organismo.barra_energia < umbral:
        return matriz
    if posiciones_adyacentes is None:
        posiciones_adyacentes = obtener_posiciones_adyacentes(matriz, fila, columna)
    if not posiciones_adyacentes:
        return matriz
    vacias = filtrar_posiciones_vacias(matriz, posiciones_adyacentes)
    if vacias:
        (nueva_fila, nueva_columna) = vacias[0]
        matriz[nueva_fila][nueva_columna] = constructor_descendiente()
        organismo.barra_energia = organismo.barra_energia // 2
    return matriz


# Función recursiva para procesar cada celda de la matriz en un ciclo
def procesar_celda(matriz, fila, columna):
    tamanio = len(matriz)
    if fila >= tamanio:
        return matriz
    if columna >= tamanio:
        return procesar_celda(matriz, fila + 1, 0)
    celda = matriz[fila][columna]
    if celda is None or getattr(celda, "movido", False):
        return procesar_celda(matriz, fila, columna + 1)
    if isinstance(celda, Depredador):
        objetivo = obtener_presa_visible(matriz, fila, columna)
        if objetivo is not None:
            fila_objetivo, columna_objetivo, _ = objetivo
            cambio_fila = signo(fila_objetivo - fila)
            cambio_columna = signo(columna_objetivo - columna)
            nueva_fila = fila + cambio_fila
            nueva_columna = columna + cambio_columna
            if 0 <= nueva_fila < tamanio and 0 <= nueva_columna < tamanio:
                destino = matriz[nueva_fila][nueva_columna]
                if destino is None or isinstance(destino, Presa):
                    if isinstance(destino, Presa):
                        celda.barra_energia += 2
                    matriz[nueva_fila][nueva_columna] = celda
                    celda.movido = True
                    matriz[fila][columna] = None
        else:
            posiciones_adyacentes = obtener_posiciones_adyacentes(matriz, fila, columna)
            celdas_vacias = filtrar_posiciones_vacias(matriz, posiciones_adyacentes)
            if celdas_vacias:
                (nueva_fila, nueva_columna) = random.choice(celdas_vacias)
                matriz[nueva_fila][nueva_columna] = celda
                celda.movido = True
                matriz[fila][columna] = None
        celda.barra_energia -= 1
        if celda.barra_energia <= 0:
            matriz[fila][columna] = None
        else:
            matriz = intentar_reproducir(
                matriz, fila, columna, celda, 8, lambda: Depredador()
            )
    elif isinstance(celda, Presa):
        posiciones_adyacentes = obtener_posiciones_adyacentes(matriz, fila, columna)

        def buscar_planta(lista_posiciones, indice):
            if indice >= len(lista_posiciones):
                return None
            (fila_objetivo, columna_objetivo) = lista_posiciones[indice]
            if isinstance(matriz[fila_objetivo][columna_objetivo], Planta):
                return (fila_objetivo, columna_objetivo)
            else:
                return buscar_planta(lista_posiciones, indice + 1)

        objetivo = buscar_planta(posiciones_adyacentes, 0)
        if objetivo is not None:
            fila_objetivo, columna_objetivo = objetivo
            celda.barra_energia += 2
            matriz[fila_objetivo][columna_objetivo] = celda
            celda.movido = True
            matriz[fila][columna] = None
        else:
            vacias = filtrar_posiciones_vacias(matriz, posiciones_adyacentes)
            if vacias:
                (fila_vacia, columna_vacia) = random.choice(vacias)
                matriz[fila_vacia][columna_vacia] = celda
                celda.movido = True
                matriz[fila][columna] = None
        celda.barra_energia -= 1
        if celda.barra_energia <= 0:
            matriz[fila][columna] = None
        else:
            matriz = intentar_reproducir(
                matriz, fila, columna, celda, 6, lambda: Presa()
            )
    return procesar_celda(matriz, fila, columna + 1)


# Función recursiva para reiniciar la bandera "movido" en cada organismo de la matriz
def reiniciar_movimiento(matriz, fila=0, columna=0):
    tamanio = len(matriz)
    if fila >= tamanio:
        return matriz
    if columna >= tamanio:
        return reiniciar_movimiento(matriz, fila + 1, 0)
    if matriz[fila][columna] is not None:
        matriz[fila][columna].movido = False
    return reiniciar_movimiento(matriz, fila, columna + 1)


# Función recursiva para regenerar plantas cada 3 ciclos en celdas vacías
def regenerar_plantas(matriz, fila=0, columna=0):
    tamanio = len(matriz)
    if fila >= tamanio:
        return matriz
    if columna >= tamanio:
        return regenerar_plantas(matriz, fila + 1, 0)
    if matriz[fila][columna] is None:
        if random.random() < 0.3:
            matriz[fila][columna] = Planta()
    return regenerar_plantas(matriz, fila, columna + 1)


# Función recursiva que determina si aún existen organismos (Depredador o Presa) en el ecosistema
def existen_organismos(matriz, fila=0, columna=0):
    tamanio = len(matriz)
    if fila >= tamanio:
        return False
    if columna >= tamanio:
        return existen_organismos(matriz, fila + 1, 0)
    celda = matriz[fila][columna]
    if celda is not None and (
        isinstance(celda, Depredador) or isinstance(celda, Presa)
    ):
        return True
    return existen_organismos(matriz, fila, columna + 1)


# Función recursiva para generar una fila aleatoria de tamaño dado
def crear_fila_aleatoria(
    tamanio,
    columna=0,
    lista_fila=None,
    probabilidad_de_predador=0.1,
    probabilidad_de_presa=0.2,
    probabilidad_de_planta=0.3,
):
    if lista_fila is None:
        lista_fila = []
    if columna >= tamanio:
        return lista_fila
    valor_aleatorio = random.random()
    if valor_aleatorio < probabilidad_de_predador:
        lista_fila.append(Depredador())
    elif valor_aleatorio < probabilidad_de_predador + probabilidad_de_presa:
        lista_fila.append(Presa())
    elif (
        valor_aleatorio
        < probabilidad_de_predador + probabilidad_de_presa + probabilidad_de_planta
    ):
        lista_fila.append(Planta())
    else:
        lista_fila.append(None)
    return crear_fila_aleatoria(
        tamanio,
        columna + 1,
        lista_fila,
        probabilidad_de_predador,
        probabilidad_de_presa,
        probabilidad_de_planta,
    )


# Función recursiva para generar el ecosistema aleatorio (matriz) de tamaño n x n
def crear_ecosistema_aleatorio(
    tamanio,
    fila=0,
    matriz=None,
    probabilidad_de_predador=0.1,
    probabilidad_de_presa=0.2,
    probabilidad_de_planta=0.3,
):
    if matriz is None:
        matriz = []
    if fila >= tamanio:
        return matriz
    nueva_fila = crear_fila_aleatoria(
        tamanio,
        0,
        None,
        probabilidad_de_predador,
        probabilidad_de_presa,
        probabilidad_de_planta,
    )
    matriz.append(nueva_fila)
    return crear_ecosistema_aleatorio(
        tamanio,
        fila + 1,
        matriz,
        probabilidad_de_predador,
        probabilidad_de_presa,
        probabilidad_de_planta,
    )


# Función recursiva principal de simulación, con una pausa entre ciclos
def simular_ecosistema(matriz, ciclo, ciclos_maximos):
    if ciclo > ciclos_maximos or not existen_organismos(matriz):
        print("Fin de la simulación en el ciclo", ciclo)
        imprimir_matriz(matriz)
        return matriz
    print("Ciclo", ciclo)
    imprimir_matriz(matriz)
    time.sleep(1)  # Pausa de 1 segundo entre ciclos
    matriz = procesar_celda(matriz, 0, 0)
    matriz = reiniciar_movimiento(matriz)
    if ciclo % 3 == 0:
        matriz = regenerar_plantas(matriz)
    return simular_ecosistema(matriz, ciclo + 1, ciclos_maximos)


# Generar aleatoriamente un ecosistema (matriz) de 5x5 con las siguientes probabilidades:
# 1% para depredadores, 30% para presas, 30% para plantas y el movimientos_posibles celdas vacías.
ecosistema = crear_ecosistema_aleatorio(
    5,
    probabilidad_de_predador=0.01,
    probabilidad_de_presa=0.3,
    probabilidad_de_planta=0.3,
)

simular_ecosistema(ecosistema, 1, 50)
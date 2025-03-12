import random

def PrintBorderMatrix(matrix, fila = 0, columna = 0, FindElements = []):

    if (fila == len(matrix)):
        return FindElements
    if (columna == len(matrix[fila])):
        return PrintBorderMatrix(matrix,fila+1,0)
    if (fila == 0 or fila == len(matrix)-1 or columna == 0 or columna == len(matrix[fila])-1):
        print(matrix[fila][columna])
        return PrintBorderMatrix(matrix,fila,columna+1,FindElements)
    return PrintBorderMatrix(matrix,fila,columna+1,FindElements)


def CreateMatrixWithRandom(n, m):

    return [[random.randint(0, 100) for j in range(m)] for i in range(n)] 

matriz = CreateMatrixWithRandom(5,6)

print(matriz)

print(PrintBorderMatrix(matriz))
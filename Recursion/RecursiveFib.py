def Fibo(n:int) -> int:
    #Ambos condicionales son los casos bases, esto es para que  la recursividad lleguen a un punto en donde pueda finalizar
    if n == 0:
        return 0
    if n == 1:
        return n
    return Fibo(n-1) + Fibo(n-2)

print(Fibo(100))
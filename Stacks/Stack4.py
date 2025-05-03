class Stack:

    def __init__(self):
        self.Stack = []

    def Push(self, Item):
        self.Stack.append(Item)

    def Pop(self):
        if self.__len__() <= 0:
            return None
        else:
            aux = self.Stack[-1]
            self.Stack.pop()
            return aux

    def Top(self):
        if self.__len__() <= 0:
            return None
        else:
            return self.Stack[-1]

    def __len__(self):
        return len(self.Stack)

    def __repr__(self):
        return str(self.Stack)
    

cola = Stack()
a = "3 4 + 5 *"

for i in range(len(a)):
    cola.Push(a[i])

print(cola)


def RPN(ItStack):
    auxStack = Stack()
    for _ in range(len(ItStack)):
        auxvar= ItStack.Pop()
        if auxvar == " ":
            continue
        elif auxvar == "*" or auxvar == "+" or auxvar == "/" or auxvar == "-":
            auxStack.Push(auxvar)
        
        try: 
            if  isinstance(int(auxvar), int):
                auxStack.Push(auxvar)
        except: continue

    for _ in range(len(auxStack)):
        auxvar = auxStack.Pop()
        if len(ItStack) == 2:
            if auxvar == "+":
                First = ItStack.Pop()
                second = ItStack.Pop()
                ItStack.Push(First + second)
            if auxStack == "*":
                First = ItStack.Pop()
                second = ItStack.Pop()
                ItStack.Push(First * second)
            if auxStack == "/":
                First = ItStack.Pop()
                second = ItStack.Pop()
                ItStack.Push(First / second)

        try: 
            if  isinstance(int(auxvar), int):
                ItStack.Push(auxvar)
        except: continue


    return ItStack

a= RPN(cola)
print(a)


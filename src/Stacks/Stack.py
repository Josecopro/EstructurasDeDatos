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
    

def GetStack(ItStack: Stack):
    AuxStack = Stack()
    for _ in range(len(ItStack)):
        Item = ItStack.Pop()
        AuxStack.Push(Item)
        print(Item)

    for _ in range(len(AuxStack)):
        ItStack.Push(AuxStack.Pop())


cola = Stack()

cola.Push(1)
cola.Push(2)
cola.Push(3)
cola.Push(4)
cola.Push(5)

a = GetStack(cola)

print(cola)
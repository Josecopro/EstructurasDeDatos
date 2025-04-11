from dataclasses import dataclass

@dataclass
class Node:
    Value: int 
    Next: "Node" = None


@dataclass
class LinkedList:
    Head: Node = None
    Tail: Node = None
    Size: int = 0

    def AppendFirst(self, Value):
        NewNode = Node(Value)
        if self.Size == 0:
            self.Head = NewNode
            self.Tail = NewNode
            self.Size += 1
            return None
        NewNode.Next = self.Head
        self.Head = NewNode
        self.Size += 1


    def AppendLast(self, Value):
        NewNode = Node(Value)
        if self.Size == 0:
            self.Head = NewNode
            self.Tail = NewNode
            self.Size += 1
            return None
        self.Tail.Next = NewNode
        self.Tail = NewNode
        self.Size += 1



    def RemoveFirst(self):
        if self.Size != 0:
            ReturnValue = self.Head
            Aux = self.Head.Next
            self.Head.Next = None
            self.Head = Aux
            self.Size -=1
            return ReturnValue.Value
        print("Paila la lista esta llena")


    def SelectFirst(self):
        if self.Size != 0:
            return self.Head.Value
        print("Ta vacia loco")




class Queue:

    def __init__(self):
        self.queue = LinkedList()
        self.Size = 0 

    def Enqueue(self, Item):
            self.Size += 1
            self.queue.AppendFirst(Item)

    def Dequeue(self):
        if self.Size != 0:
            self.Size -= 1
            return self.queue.RemoveFirst()
        print("Ta vacio pa")

    def First(self):
        if self.Size != 0:
            return self.queue.SelectFirst()
        print("Ta vacio pa")    


class Stack:

    def __init__(self):
        self.Stack = LinkedList()
        self.Size = 0 

    def Push(self, Item):
        self.Stack.AppendLast(Item)
        self.Size += 1

    def Pop(self):
        if self.Size <= 0:
            return None
        else:
            self.Size -= 1
            return self.Stack.RemoveFirst()

    def Top(self):
        if self.Size <= 0:
            return None
        else:
            return self.Stack.SelectFirst()


cola = Queue()

cola.Enqueue(1)
cola.Enqueue(2)
cola.Enqueue(3)
cola.Enqueue(4)
#print(cola.First())
#print(cola.Dequeue())
#print(cola.First())


pila = Stack()

pila.Push(1)
print(pila.Top())
pila.Push(2)
print(pila.Top())




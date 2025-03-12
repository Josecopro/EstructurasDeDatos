class FullQueue(Exception):
    def __init__(self):
        super().__init__("La fila esta llena pa")

class CircleQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0

    def Enqueue(self, Element):
            if self.capacity == self.head:
                    self.head = 0
            if self.queue[self.head] != None:
                raise FullQueue()
            self.queue[self.head] = Element
            self.head += 1
    
             
            
    def Dequeue(self):
        if self.tail == self.capacity:
            self.tail = 0
            self.queue[self.tail] = None
        else:
            self.queue[self.tail] = None
            self.tail += 1
        return self.queue[self.tail - 1]

    def show(self):
              print(self.queue)

    def First(self):
         return self.queue[self.tail]


cola = CircleQueue(7)
cola.Enqueue(1)
cola.Enqueue(1)
cola.Enqueue(1)
cola.Enqueue(1)
cola.Enqueue(1)
cola.Enqueue(1)
cola.Enqueue(1)
cola.Dequeue()
cola.Dequeue()
cola.Dequeue()
cola.Dequeue()
cola.Dequeue()
cola.Dequeue()
cola.Dequeue()
cola.Enqueue(1)
cola.Dequeue()

cola.show()


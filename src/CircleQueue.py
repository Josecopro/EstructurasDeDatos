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
        self.queue[self.tail] = None
        self.tail += 1

    def show(self):
              print(self.queue)



cola = CircleQueue(7)

cola.Enqueue(1)
cola.Enqueue(2)
cola.Dequeue()
cola.Enqueue(3)
cola.Enqueue(5)
cola.Enqueue(6)
cola.Enqueue(10)
cola.Enqueue(11)
cola.Enqueue(12)
cola.Dequeue()
cola.Dequeue()
cola.Enqueue(1)

cola.show()


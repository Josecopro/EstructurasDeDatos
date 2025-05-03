


class Queue:

    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0

    def Enqueue(self, Item):
            self.queue[self.head] = Item
            self.head += 1

    def Dequeue(self):
        aux = self.queue[self.tail]
        self.queue[self.tail] = None
        self.tail += 1
        
        return aux
        

    def First(self):
        if self.tail == self.head:
            return None
        return self.queue[self.tail]

    def Show(self):
        print(self.queue)


Size = 8

def InverseSecondHalf(FirstQueue, Counter = 1, AuxQueue = None):
    if Counter == FirstQueue.capacity:
         return FirstQueue
    mid = FirstQueue.capacity // 2
    AuxQueue = Queue(mid)
    if Counter < mid:
        AuxQueue.Enqueue(FirstQueue.First())
        FirstQueue.Dequeue()
        return InverseSecondHalf(FirstQueue, Counter + 1, AuxQueue)
    else:
        AuxQueue.Enqueue(FirstQueue.Dequeue())
        return InverseSecondHalf(FirstQueue, Counter + 1 , AuxQueue)
         


cola = Queue(Size)

for i in range(Size):
     cola.Enqueue(i)
     cola.Show()

InverseSecondHalf(cola)


cola.Show()





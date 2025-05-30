


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
        self.queue[self.tail] = None
        self.tail += 1

    def Show(self):
        print(self.queue)


Size = 8

def InverseSecondHalf(Capacity, FirstQueue):
    mid = Capacity // 2
    AuxQueue = Queue(Capacity)
    for i in range(Capacity):
        if i < mid:
             AuxQueue.Enqueue(FirstQueue.queue[i])
        else:
            AuxQueue.Enqueue(FirstQueue.queue[Capacity - i - 5])

    return AuxQueue
    
    
        

cola = Queue(Size)

for i in range(Size):
     cola.Enqueue(i)
     cola.Show()

InverseSecondHalf(Size,cola).Show()





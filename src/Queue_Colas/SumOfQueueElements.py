class FullQueue(Exception):
    def __init__(self):
        super().__init__("La fila esta llena pa")

class Queue:
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
        return self.queue[self.tail]

    def Show(self):
              print(self.queue)

    def First(self):
         return self.queue[self.tail]

def SearchSum(colita: Queue, SearchNumber, ElementCounter = 1, AuxNum = 0):
    if ElementCounter == colita.capacity:
         print("No hay números que sumen: ", SearchNumber)
         return None
    for i in colita.queue:
        AuxNum = colita.Dequeue()
        if AuxNum + colita.First() == SearchNumber:
            return (AuxNum , colita.First())
        else:
            colita.Dequeue()
            return SearchSum(colita, SearchNumber , ElementCounter)
    return SearchNumber(colita, SearchNumber, ElementCounter + 1, AuxNum = colita.Dequeue())
        
Size = 8

cola = Queue(Size)

for i in range(Size):
     
        cola.Enqueue(i)
        cola.Show()

print(SearchSum(cola, 3))


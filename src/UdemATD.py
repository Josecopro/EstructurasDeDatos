class UdeM:
    def __init__(self):
        self.list = {}
        self.lastkeyadd = 0
        self.firstkey = 0 
        self.size:int = len(self.list)

    def add(self, item: str) -> None:
        self.list[self.lastkeyadd] = [item]
        self.lastkeyadd = self.firstkey + 1 //2


    def dequeue(self):
        if self.is_empty():
            return None
        item = self.queue.pop(self.lastkeyadd)
        self.first_key += 1
        return item

    def is_empty(self):
        return self.first_key == self.next_key
    
    def __str__(self):
        return str(self.list)


udem = UdeM()

udem.add("1")
udem.add("2")
udem.add("3")
udem.add("4")
udem.add("5")
udem.add("6")
print(udem)
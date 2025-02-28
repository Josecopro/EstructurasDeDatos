class Queue:
    def __init__(self):
        self.queue = {}
        self.next_key = 0
        self.first_key = 0

    def enqueue(self, item):
        self.queue[self.next_key] = item
        self.next_key += 1

    def dequeue(self):
        if self.is_empty():
            return None
        item = self.queue.pop(self.first_key)
        self.first_key += 1
        return item

    def is_empty(self):
        return self.first_key == self.next_key

    def first(self):
        if self.is_empty():
            return None
        return self.queue[self.first_key]
    
    def __str__(self):
        auxlist = []
        for key in self.queue:
            auxlist.append(self.queue[key])
        return str(auxlist)
    
    def uwu(self):
        return self.queue


q = Queue()

q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
q.enqueue(4)
q.enqueue(5)
q.dequeue()
q.dequeue()

print(q)

print(q.first())

print(q.uwu())
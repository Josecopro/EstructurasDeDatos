from dataclasses import dataclass
import time
from random import randint

@dataclass
class Song:
    Duration: int
    Title: str
    Artist: str
    def __repr__(self):
        return f"Cancion: {self.Title}, del artista: {self.Artist}, duracion: {self.Duration}"

@dataclass
class Node:
    Value: Song 
    Next: "Node" = None
    Prev: "Node" = None
    
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
            NewNode.Prev = NewNode
            self.Head.Next = self.Tail
            self.Tail.Next = self.Head
        else:
            NewNode.Next = self.Head
            NewNode.Prev = self.Tail
            self.Head.Prev = NewNode
            self.Tail.Next = NewNode
            self.Head = NewNode
        self.Size += 1

    def AppendLast(self, Value):
        NewNode = Node(Value)
        if self.Size == 0:
            self.Head = NewNode
            self.Tail = NewNode
            self.Head.Next = self.Tail
            self.Tail.Next = self.Head
            self.Head.Prev = self.Tail
            self.Tail.Prev = self.Head
        else:
            NewNode.Prev = self.Tail
            NewNode.Next = self.Head
            self.Tail.Next = NewNode
            self.Head.Prev = NewNode
            self.Tail = NewNode
        self.Size += 1

    def RemoveFirst(self):
        if self.Size != 0:
            ReturnValue = self.Head
            if self.Size == 1:
                self.Head = None
                self.Tail = None
            else:
                Aux = self.Head.Next
                self.Head.Next = None
                self.Head.Prev = None
                self.Head = Aux
                self.Head.Prev = self.Tail
                self.Tail.Next = self.Head
            self.Size -= 1
            print("DEBUG: cancion eliminada", ReturnValue.Value)
            return ReturnValue.Value
        print("Paila la lista esta vacia")

    def Remove(self, node):
        if self.Size != 0:
            if node == self.Head:
                return self.RemoveFirst()
            elif node == self.Tail:
                self.Tail = self.Tail.Prev
                self.Tail.Next = self.Head
                self.Head.Prev = self.Tail
            else:
                node.Prev.Next = node.Next
                node.Next.Prev = node.Prev
            node.Next = None
            node.Prev = None
            self.Size -= 1
            print("DEBUG: cancion eliminada", node.Value)
            return node.Value
        print("Paila la lista esta vacia")

    def SelectFirst(self):
        if self.Size != 0:
            return self.Head.Value
        print("Ta vacia loco")

    def __iter__(self):
        self.current = self.Head
        self.start = True
        return self

    def __next__(self):
        if self.current is None or (self.current == self.Head and not self.start):
            raise StopIteration
        else:
            self.start = False
            data = self.current.Value
            self.current = self.current.Next
            return data

    def __contains__(self, item):
        for data in self:
            if data.Title == item:
                return True
        return False
    
    def __repr__(self):
        current = self.Head
        result = []
        if current is not None:
            while True:
                result.append(str(current.Value))
                current = current.Next
                if current == self.Head:
                    break
        return "\n".join(result)





#reate a LinkedList instance
playlist = LinkedList()
# Add songs to the playlist
playlist.AppendLast(Song(210, "Song 1", "Artist A"))
playlist.AppendLast(Song(180, "Song 2", "Artist B"))
playlist.AppendLast(Song(240, "Song 3", "Artist C"))
playlist.AppendLast(Song(200, "Song 4", "Artist D"))
print(playlist.Head)
# Print the playlist
print("Playlist:")
print(playlist)


def Randomize():
    counter = 0
    SongPos = {}
    for song in playlist:
        SongPos[counter] = [song, False]
        counter += 1

    while True:
        random = randint(0, playlist.Size)
        if SongPos[random][1] == False:
            SongPos[random][1] == True
            return SongPos[random]




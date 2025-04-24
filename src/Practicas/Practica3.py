from dataclasses import dataclass
import time
import threading

@dataclass
class Song:
    Duration: int
    Title: str
    Artist: str

    def __repr__(self):
        return f"Cancion: {self.Title}, del artista: {self.Artist}, duracion: {self.Duration} segundos"

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

@dataclass
class MediaPlayer:
    spotify = LinkedList()
    IsPlaying = False
    stop_event = threading.Event()
    skip_event = threading.Event()

    def AddSong(self, song: Song):
        if song.Title in self.spotify:
            return f"La cancion: {song.Title} ya esta en la playlist"
        self.spotify.AppendFirst(song)

    def RemoveSong(self, song: Song):
        counter = 0 
        if song in self.spotify:
            SecHead = self.spotify.Head
            if SecHead.Value.Title == song:
                self.spotify.RemoveFirst()
                return None
            while counter < self.spotify.Size:
                SecHead = SecHead.Next
                if SecHead.Value.Title == song:
                    self.spotify.Remove(SecHead)
                    return None
                counter += 1
        print("no se encontro la cancion: ", song)

    def ActualSong(self):
        return self.spotify.Head.Value

    def SkipSong(self):
        if self.spotify.Size > 1:
            self.spotify.Head = self.spotify.Head.Next
            self.skip_event.set()  
        else:
            print("No hay más canciones para saltar.")

    def StartPlaylist(self):
        self.IsPlaying = True
        self.stop_event.clear()
        self.skip_event.clear()

        def play_songs():
            while self.IsPlaying and self.spotify.Size > 0:
                current_song = self.spotify.Head.Value
                print(f"Reproduciendo actualmente: {current_song}")
                start_time = time.time()

                while time.time() - start_time < current_song.Duration:
                    if self.stop_event.is_set():
                        print("Reproducción detenida.")
                        return
                    if self.skip_event.is_set():
                        self.skip_event.clear()
                        break
                    time.sleep(1)

                self.spotify.Head = self.spotify.Head.Next

            print("DEBUG: Playlist terminada o reproducción detenida.")

        threading.Thread(target=play_songs, daemon=True).start()

    def StopPlaylist(self):
        self.IsPlaying = False
        self.stop_event.set()

    def __repr__(self):
        playlist = "\n".join([f"{idx + 1}. {song.Title} - {song.Artist} ({song.Duration}s)" 
                    for idx, song in enumerate(self.spotify)])
        return (
            "=========================\n"
            "      Media Player       \n"
            "=========================\n"
            f"Playlist:\n{playlist}\n"
            "=========================\n"
            f"Total de canciones: {self.spotify.Size}\n"
            "========================="
        )

@dataclass
class Controler:
    OwnMediaPlayer = MediaPlayer()

    def SelectSong(self):
        Flag = "si"
        while True:
            if Flag.lower() == "si":
                Title = str(input("Ingrese el titulo de la cancion: "))
                Duration = int(input("Ingrese la duración de la canción: "))
                Artist = str(input("Ingrese el artista de la canción: "))
                self.OwnMediaPlayer.AddSong(Song(Duration, Title, Artist))
            else: 
                break
            Flag = str(input("Desea Ingresar mas canciones? \n Si / No : "))

    def StartPlaying(self):
        if self.OwnMediaPlayer.spotify.Size != 0:
            self.OwnMediaPlayer.StartPlaylist()
        else:
            print("No existen canciones agregadas")

    def StopPlaying(self):
        self.OwnMediaPlayer.StopPlaylist()

    def SkipCurrentSong(self):
        self.OwnMediaPlayer.SkipSong()

    def CurrentSong(self):
        if self.OwnMediaPlayer.spotify.Size != 0:
            print(self.OwnMediaPlayer.ActualSong())
        else:
            print("No existen canciones agregadas")

    def PrincipalMenu(self):
        print("Bienvenido al reproductor de música, Seleccione alguna de las opciones: ")
        
        while True:
            print("1. Ingrese canciones \n2. Revise la playlist \n3. Elimine alguna canción \n4. Revise la canción actual \n5. Reproducir playlist \n6. Detener reproducción \n7. Saltar canción \n8. Salir del reproductor")
            Selector = int(input("Seleccione una opcion: "))

            if Selector == 1:
                self.SelectSong()
            elif Selector == 2:
                print(self.OwnMediaPlayer)
            elif Selector == 3:
                SongTitle = str(input("Ingrese el título de la canción a eliminar: "))
                self.OwnMediaPlayer.RemoveSong(SongTitle)
            elif Selector == 4:
                self.CurrentSong()
            elif Selector == 5:
                self.StartPlaying()
            elif Selector == 6:
                self.StopPlaying()
            elif Selector == 7:
                self.SkipCurrentSong()
            elif Selector == 8:
                self.StopPlaying()
                break
            else:
                print("Opción no válida. Intente de nuevo.")

SpotifyGratis = Controler()

SpotifyGratis.PrincipalMenu()
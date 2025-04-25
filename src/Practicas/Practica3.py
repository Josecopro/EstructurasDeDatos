from dataclasses import dataclass, field
import time
import threading
from random import randint

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
class SubPlaylist:
    name: str
    playlist: LinkedList = field(default_factory=LinkedList)
    
    def add_song(self, song: Song):
        self.playlist.AppendLast(song)
        
    def __repr__(self):
        return f"SubPlaylist: {self.name} ({self.playlist.Size} canciones)"

@dataclass
class MediaPlayer:
    spotify = LinkedList()
    IsPlaying = False
    stop_event = threading.Event()
    skip_event = threading.Event()
    SongPos: dict = field(default_factory=dict)
    SongPosCounter: int = 0
    RandomSongsPlayed: int = 0
    subplaylists: dict = field(default_factory=dict)  

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
    
    def AddSubPlaylistToMain(self, subplaylist_name):
        """Añade las canciones de una subplaylist a la playlist principal"""
        if subplaylist_name not in self.subplaylists:
            print(f"No existe una subplaylist llamada '{subplaylist_name}'")
            return

        subplaylist = self.subplaylists[subplaylist_name]
        current_node = subplaylist.playlist.Head
        if not current_node:
            print(f"La subplaylist '{subplaylist_name}' está vacía.")
            return

        for _ in range(subplaylist.playlist.Size):
            self.spotify.AppendLast(current_node.Value)
            current_node = current_node.Next

        print(f"Subplaylist '{subplaylist_name}' añadida a la playlist principal como canciones normales.")


    def SkipSong(self):
        if self.spotify.Size > 1:
            self.spotify.Head = self.spotify.Head.Next
            self.skip_event.set()  
        else:
            print("No hay más canciones para saltar.")
    def CreateSubPlaylist(self, name):
        """Crea una nueva subplaylist con el nombre dado"""
        if name in self.subplaylists:
            print(f"Ya existe una subplaylist llamada '{name}'")
            return None
        
        new_subplaylist = SubPlaylist(name)
        self.subplaylists[name] = new_subplaylist
        return new_subplaylist
    
    def AddSongToSubPlaylist(self, subplaylist_name, song):
        """Añade una canción a una subplaylist existente"""
        if subplaylist_name not in self.subplaylists:
            print(f"No existe una subplaylist llamada '{subplaylist_name}'")
            return
        
        self.subplaylists[subplaylist_name].add_song(song)
        print(f"Canción '{song.Title}' añadida a la subplaylist '{subplaylist_name}'")
    
    def AddSubPlaylistToMain(self, subplaylist_name):
        """Añade una subplaylist a la playlist principal"""
        if subplaylist_name not in self.subplaylists:
            print(f"No existe una subplaylist llamada '{subplaylist_name}'")
            return
        
        subplaylist_marker = Song(0, f"SUBPLAYLIST:{subplaylist_name}", "")
        self.spotify.AppendLast(subplaylist_marker)
        print(f"Subplaylist '{subplaylist_name}' añadida a la playlist principal")
    
    def StartPlaylist(self, IsRandom: bool):
        self.IsPlaying = True
        self.stop_event.clear()
        self.skip_event.clear()

        def play_songs():
            while self.IsPlaying and self.spotify.Size > 0:
                current_song = self.spotify.Head.Value
                print("=====================================")
                print(f"\n Reproduciendo actualmente: {current_song} \n")
                print("=====================================")
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

        threading.Thread(target=play_songs, daemon=True).start()


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

    def StartPlaying(self, IsRandom: bool):
        if self.OwnMediaPlayer.spotify.Size != 0:
            self.OwnMediaPlayer.StartPlaylist(IsRandom)
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

    def CreateSubPlaylist(self):
        name = input("Ingrese el nombre para la nueva subplaylist: ")
        self.OwnMediaPlayer.CreateSubPlaylist(name)
    
    def AddSongToSubPlaylist(self):
        if len(self.OwnMediaPlayer.subplaylists) == 0:
            print("No hay subplaylists creadas. Cree una primero.")
            return
            
        print("Subplaylists disponibles:")
        for name in self.OwnMediaPlayer.subplaylists:
            print(f"- {name}")
            
        subplaylist_name = input("Ingrese el nombre de la subplaylist: ")
        if subplaylist_name not in self.OwnMediaPlayer.subplaylists:
            print(f"No existe una subplaylist llamada '{subplaylist_name}'")
            return
            
        Title = str(input("Ingrese el titulo de la cancion: "))
        Duration = int(input("Ingrese la duración de la canción: "))
        Artist = str(input("Ingrese el artista de la canción: "))
        song = Song(Duration, Title, Artist)
        
        self.OwnMediaPlayer.AddSongToSubPlaylist(subplaylist_name, song)
    
    def AddSubPlaylistToMain(self):
        if len(self.OwnMediaPlayer.subplaylists) == 0:
            print("No hay subplaylists creadas. Cree una primero.")
            return
            
        print("Subplaylists disponibles:")
        for name in self.OwnMediaPlayer.subplaylists:
            print(f"- {name}: {self.OwnMediaPlayer.subplaylists[name].playlist.Size} canciones")
            
        subplaylist_name = input("Ingrese el nombre de la subplaylist a añadir a la playlist principal: ")
        self.OwnMediaPlayer.AddSubPlaylistToMain(subplaylist_name)
    

    def PrincipalMenu(self):
        print("Bienvenido al reproductor de música, Seleccione alguna de las opciones: ")
        
        while True:
            print("1. Ingrese canciones \n2. Revise la playlist \n3. Elimine alguna canción \n4. Revise la canción actual \n5. Reproducir playlist \n6. Detener reproducción \n7. Saltar canción \n8. Reproducir en orden aleatorio \n9. Crear subplaylist \n10. Añadir canción a subplaylist \n11. Añadir subplaylist a playlist principal \n12. Salir")
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
                self.StartPlaying(IsRandom=False)
            elif Selector == 6:
                self.StopPlaying()
            elif Selector == 7:
                self.SkipCurrentSong()
            elif Selector == 8:
                self.StartPlaying(IsRandom=True)
            elif Selector == 9:
                self.CreateSubPlaylist()
            elif Selector == 10:
                self.AddSongToSubPlaylist()
            elif Selector == 11:
                self.AddSubPlaylistToMain()
            elif Selector == 12:
                break
            else:
                print("Opción no válida. Intente de nuevo.")

SpotifyGratis = Controler()

SpotifyGratis.PrincipalMenu()
class Graph:
    def __init__(self):
        self.adj_list: dict[(int,list[int])] = {}
        self.size = 0
        self.nonweight_value = 0 #valor no representativo
        self.relation_value = 1

    def add_vertex(self, vertex_value):
        if(vertex_value in self.adj_list):
            return

        self.adj_list[vertex_value] = []
        self.size += 1

    def add_edge(self, vertex_1, vertex_2, directed = True, weight: int = None):
        #si no existen los vértices, los creo...
        if(vertex_1 not in self.adj_list):
            self.add_vertex(vertex_1)

        if(vertex_2 not in self.adj_list):
            self.add_vertex(vertex_2)


        #relation_weight = self.relation_value if weight is None else weight

        if(not directed):
            if(vertex_1 not in self.adj_list[vertex_2]):
                self.adj_list[vertex_2].append(vertex_1)

        if(vertex_2 not in self.adj_list[vertex_1]):
            self.adj_list[vertex_1].append(vertex_2)

    def __repr__(self):
        return str(self.adj_list)
  
  
    def DFS(self, current, visited=None):
        if visited is None:
            visited = []

        if current not in self.adj_list:
            return

        visited.append(current)

        for neighbor in self.adj_list[current]:
            if neighbor not in visited:
                self.DFS(neighbor, visited)

        return visited
    
    def IsCiclic(self, current, visited = None):
        if visited is None:
            visited = []
        
        if current not in self.adj_list:
            return

        if current in visited:
            print("Ola")
            return True

        visited.append(current)

        for neighbor in self.adj_list[current]:
            if neighbor in visited:
                print("Ola recursivo")
                return True
            if self.IsCiclic(neighbor, visited):
                return True

        return False


g = Graph()
g.add_edge(0, 1, directed=True)
g.add_edge(0, 2, directed=True)
g.add_edge(1, 3, directed=True)
g.add_edge(1, 4, directed=True)
g.add_edge(2, 5, directed=True)
g.add_edge(2, 6, directed=True)
g.add_edge(3, 0, directed=True)  # Adding a cycle: 0 -> 1 -> 3 -> 0
g.add_edge(4, 2, directed=True)  # Adding another cycle: 0 -> 1 -> 4 -> 2 -> 0

print(g.adj_list)
print("====")
print(g.IsCiclic(0))


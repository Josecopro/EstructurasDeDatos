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

g = Graph()
g.add_edge(2,10, directed = False)
g.add_edge(3,1, directed = False)
g.add_edge(4,6)
g.add_edge(10,3)
print(g)


def BFS(g: Graph, current: int, Visited = [], cola = []):
    cola.append(current)
    while cola:
        current = cola[0]
        if current  in Visited:
            current = cola.pop(0)
        else:
            cola.extend(g.adj_list[current])
            Visited.append(current)
    return Visited
  
var = BFS(g, 10)

print(var)
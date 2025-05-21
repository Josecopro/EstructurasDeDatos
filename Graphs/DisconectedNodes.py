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

# Primer conjunto de nodos conectados entre sí
g = Graph()
g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("B", "X")

# Segundo conjunto de nodos conectados entre sí, pero sin conexión con el primero
g.add_edge("X", "Y")
g.add_edge("Y", "Z")
g.add_vertex("W")

print(g)


def DisconectedNodes(g:Graph):
    ConectedNodes = 0
    valores = []
    TotalNodes = set()
    for nodes in g.adj_list:
        if len(g.adj_list[nodes]) > 0:
          ConectedNodes +=1

    for nodes in g.adj_list:
        aux = g.adj_list[nodes]
        valores.extend(aux)
    

    for valor in valores:
      TotalNodes.add(valor)

    for elements in list(g.adj_list.keys()):
        TotalNodes.add(elements)

            
    return len(TotalNodes) - ConectedNodes


print(DisconectedNodes(g))

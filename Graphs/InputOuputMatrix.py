class Graph:
  def __init__(self):
    self.adj_matrix: list[list[int]] = []
    self.nodes: list[int] = []
    self.size = 0
    self.nonweight_value = 0 #valor no representativo
    self.relation_value = 1

  def add_vertex(self, vertex_value):
    if(vertex_value in self.nodes):
      return

    #agrego a la lista de nodos
    self.nodes.append(vertex_value)
    self.size += 1

    #matriz de ady.
    for row in self.adj_matrix:
      row.append(self.nonweight_value)

    self.adj_matrix.append([self.nonweight_value] * self.size)

  def add_edge(self, vertex_1, vertex_2, directed = True, weight: int = None):
    #si no existen los vértices, los creo...
    if(vertex_1 not in self.nodes):
      self.add_vertex(vertex_1)

    if(vertex_2 not in self.nodes):
      self.add_vertex(vertex_2)

    pos_v1 = self.nodes.index(vertex_1)
    pos_v2 = self.nodes.index(vertex_2)

    relation_weight = self.relation_value if weight is None else weight

    if(not directed):
      self.adj_matrix[pos_v2][pos_v1] = relation_weight
    self.adj_matrix[pos_v1][pos_v2] = relation_weight


  def DFS(self, current, visited = []):
    if(current not in self.nodes):
      return

    current_pos = self.nodes.index(current)
    neighbors = self.adj_matrix[current_pos]
    for idx, adj in enumerate(neighbors):
      neighbor = self.nodes[idx]
      if(adj == 1 and neighbor not in visited):
        visited.append(neighbor)
        self.DFS(neighbor, visited)
    return visited




  def __repr__(self):
    repr_matrix = ""
    for row in self.adj_matrix:
      repr_matrix += str(row) + "\n"

    repr_matrix += f"\n{self.nodes}"

    return repr_matrix

g = Graph()
g.add_vertex("A")
g.add_vertex("B")
g.add_vertex("C")
g.add_vertex("D")
g.add_vertex("E")
g.add_vertex("F")

# Nodo "A" tendrá 3 nodos de salida: "B", "C" y "D"
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("A", "D")

# Nodo "F" tendrá 4 nodos de entrada: "A", "B", "C", "D"
g.add_edge("A", "F")
g.add_edge("B", "F")
g.add_edge("C", "F")
g.add_edge("D", "F")

def ouput(g: Graph, Node:str):
      
    if Node in g.nodes:
        index = g.nodes.index(Node)
    lista = g.adj_matrix[index]
    result = lista.count(1)
    return result


def input(g:Graph, Node:str):
    result = 0 
    if Node in g.nodes:
        index = g.nodes.index(Node)
    lista = g.adj_matrix[index]
    for i in range(len(lista)):
      if g.adj_matrix[i][index] == 1:
        result += 1

    return result

print(input(g, "F"))

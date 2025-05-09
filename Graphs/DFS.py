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
g.add_edge("H", "O")
g.add_edge("O", "L")
g.add_edge("L", "A")
g.add_edge("D", "A")
g.add_edge("A", "E")
g.add_edge("E", "F")
g.add_edge("F", "G")
g.add_edge("G", "H")
g.add_edge("H", "A")
print(g)



def DFS(g: Graph, current: str = "", flag = True, Word = "", branch = ""):
    if flag:
        current = Word[0]
        branch += Word[0]
        flag = False 
    for references in g.adj_list[current]:   
        if references == Word[len(branch)]:
            branch += references
            DFS(g, references, flag, Word, branch)
    return branch

    

      

palabra = "HOLA"

print(DFS(g,Word =  palabra))

from dataclasses import dataclass, field

@dataclass
class Node:
    Value: int
    Children: list["Node"] = field(default_factory=list)

@dataclass
class GeneralTree:
    Root: Node = None

    def Insert(self, Parent, Child, Current=None):
        if self.Root is None:
            self.Root = Node(Parent)
            self.Root.Children.append(Node(Child))
            return True
        if self.Root.Value == Parent:
            self.Root.Children.append(Node(Child))
            return True
        if Current is None:
            Current = self.Root
        for CurrentChild in Current.Children:
            if CurrentChild.Value == Parent:
                print(f"Entra en el nodo {CurrentChild} el valor padre {Parent} y hijo {Child}")
                CurrentChild.Children.append(Node(Child))
                return True  
            if self.Insert(Parent, Child, CurrentChild):
                return True  
        return False
                




    
    def PrintTree(self, node=None, level=0):
        if node is None:
            node = self.Root
        if node is not None:
            print(" " * (level * 2) + str(node.Value))
            for child in node.Children:
                self.PrintTree(child, level + 1)

    
arbolito = GeneralTree()

arbolito.Insert(1,2)
arbolito.Insert(1,3)
arbolito.Insert(2,7)
arbolito.Insert(3,9)
arbolito.Insert(1,3)
arbolito.Insert(7,3)
arbolito.Insert(3,6)
arbolito.PrintTree()
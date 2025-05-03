from dataclasses import dataclass

@dataclass
class Node:
    Value: any  
    Next: 'Node' = None
    
Node1 = Node(1)
Node2 = Node(2)

Node3 = Node(3)
Node4 = Node(4)


Node1.Next = Node2
Node2.Next = Node3
Node3.Next = Node4

print(Node1.Next.Value)

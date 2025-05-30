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

def ReversedLinkedList(head: Node,LastNode = None, counter = 0) -> Node:
    if not isinstance(head.Next, Node):
        return head

a = ReversedLinkedList(head = Node1)

print(a)

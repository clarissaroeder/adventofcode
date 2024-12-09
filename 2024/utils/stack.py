class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self, node):
        self.top = node

    def push(self, new_node):
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top:
            popped = self.top
            self.top = self.top.next
        
        return self.top

    
    def read(self):
        return self.top.data if self.top else None
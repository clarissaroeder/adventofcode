class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

class DoublyLinkedList:
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def read(self, index):
        current_node = self.head
        current_index = 0

        while current_index < index:
            current_node = current_node.next
            current_index += 1

            # checks if the index is out of bounds
            # if index larger than the number of nodes in the list, 
            # current_node will become None when the end is reached
            if not current_node:
                return None
            
        return current_node.data
    
    def search(self, value):
        current_node = self.head
        current_index = 0

        while True:
            if current_node.data == value:
                return current_index
        
            current_node = current_node.next

            if not current_node:
                return None
            
            current_index += 1
    
    def insert(self, index, value):
        new_node = Node(value)

        if index == 0:
            new_node.next = self.head
            self.head = new_node
            return
        
        current_node = self.head
        current_index = 0

        while current_index < (index - 1):
            current_node = current_node.next
            current_index += 1

        new_node.next = current_node.next
        current_node.next = new_node

    def append(self, value):
        new_node = Node(value)

        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.previous = self.tail
            self.tail = new_node
    
    def delete(self, index):
        if index == 0:
            self.head = self.head.next
            return
        
        current_node = self.head
        current_index = 0

        while current_index < (index - 1):
            current_node = current_node.next
            current_index += 1

        current_node.next = current_node.next.next
    
    def pop(self):
        popped_node = self.head
        self.head = self.head.next
        self.head.previous = None

        return popped_node
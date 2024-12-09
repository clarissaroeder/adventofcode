import doubly_linked_list

class Queue:
    def __init__(self):
        self.data = doubly_linked_list.DoublyLinkedList()

    def enqueue(self, element):
        self.data.append(element)

    def dequeue(self):
        popped_node = self.data.pop()
        return popped_node.data

    def read(self):
        if not self.data.head:
            return None
        
        return self.data.head.data


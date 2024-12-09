class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left_child = left
        self.right_child = right

# Binary Tree Operations
def search(value, node):
    if not node or node.value == value:
        return node
    elif value < node.value:
        return search(value, node.left_child)
    else:
        return search(value, node.right_child)


def insert(value, node):
    if value < node.value:
        if not node.left_child:
            node.left_child = TreeNode(value)
        else: 
            insert(value, node.left_child)
    elif value > node.value:
        if not node.right_child:
            node.right_child = TreeNode(value)
        else:
            insert(value, node.right_child)


def replace_with_successor(node):
    successor = node.right_child

    if not successor.left_child:
        node.value = successor.value
        node.right_child = successor.right_child
        return
    
    while successor.left_child:
        successor_parent = successor
        successor = successor.left_child

    if successor.right_child:
        successor_parent.left_child = successor.right_child
    else:
        successor_parent.left_child = None

    node.value = successor.value
    return successor


def delete(value, node):
    current_node = node
    current_parent = None
    node_to_delete = None

    # find the node to be deleted, if it exists
    while current_node:
        if current_node.value == value:
            node_to_delete = current_node
            break

        current_parent = current_node
        if value < current_node.value:
            current_node = current_node.left_child
        elif value > current_node.value:
            current_node = current_node.right_child

    # if a node to be deleted has not been found, return None
    if not node_to_delete: return None

    # if the node to be deleted has two children: find the successor node
    if node_to_delete.left_child and node_to_delete.right_child:
        replace_with_successor(node_to_delete)
    # if the node to be deleted as 0 or 1 child:
    else:
        child = node_to_delete.left_child or node_to_delete.right_child

        if not current_parent:
            node_to_delete.value = child.value
            node_to_delete.left_child = child.left_child
            node_to_delete.right_child = child.right_child
        elif node_to_delete == current_parent.left_child:
            current_parent.left_child = child
        elif node_to_delete == current_parent.right_child:
            current_parent.right_child = child
    
    return node_to_delete
# Class representing a node in the Red-Black Tree
class RedBlackNode:
    def __init__(self, key, value, color="RED", left=None, right=None, parent=None):
        self.key = key  # Seat ID
        self.value = value  # User ID
        self.color = color  # 'RED' or 'BLACK'
        self.left = left  # Left child
        self.right = right  # Right child
        self.parent = parent  # Parent node

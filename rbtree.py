from rbnode import RedBlackNode


# Class representing the Red-Black Tree data structure
class RedBlackTree:
    def __init__(self):
        self.NULL_LEAF = RedBlackNode(key=None, value=None, color="BLACK")
        self.root = self.NULL_LEAF  # Initialize root as NULL_LEAF

    # Insert a new node with the given key and value
    def insert(self, key, value):
        new_node = RedBlackNode(key, value)
        new_node.left = self.NULL_LEAF
        new_node.right = self.NULL_LEAF
        parent = None
        current = self.root

        # Find the correct position to insert the new node
        while current != self.NULL_LEAF:
            parent = current
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                # Duplicate keys are not allowed
                return
        new_node.parent = parent

        # Insert the new node
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = "RED"  # New node must be red
        self.fix_insert(new_node)  # Fix the tree properties

    # Search for a node with the given key
    def search(self, key):
        return self._search_tree(self.root, key)

    # Helper method for search
    def _search_tree(self, node, key):
        if node == self.NULL_LEAF or key == node.key:
            return node
        if key < node.key:
            return self._search_tree(node.left, key)
        return self._search_tree(node.right, key)

    # Delete a node with the given key
    def delete_node(self, key):
        self.delete_node_helper(self.root, key)

    # Helper method for delete
    def delete_node_helper(self, node, key):
        z = self.NULL_LEAF  # Node to be deleted
        while node != self.NULL_LEAF:
            if node.key == key:
                z = node
            if node.key <= key:
                node = node.right
            else:
                node = node.left

        if z == self.NULL_LEAF:
            return  # Key not found in tree

        y = z
        y_original_color = y.color
        if z.left == self.NULL_LEAF:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.NULL_LEAF:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self.fix_delete(x)

    # Find the minimum node starting from the given node
    def minimum(self, node):
        while node.left != self.NULL_LEAF:
            node = node.left
        return node

    # Replace one subtree as a child of its parent with another subtree
    def rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Fix the red-black tree after insertion
    def fix_insert(self, k):
        while k.parent and k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # Uncle node
                if u.color == "RED":
                    # Case 1: Uncle is red
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # Case 2: k is left child
                        k = k.parent
                        self.right_rotate(k)
                    # Case 3: k is right child
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # Uncle node
                if u.color == "RED":
                    # Mirror case 1
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # Mirror case 2
                        k = k.parent
                        self.left_rotate(k)
                    # Mirror case 3
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    # Fix the red-black tree after deletion
    def fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                s = x.parent.right  # Sibling node
                if s.color == "RED":
                    # Case 1
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    # Case 2
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.right.color == "BLACK":
                        # Case 3
                        s.left.color = "BLACK"
                        s.color = "RED"
                        self.right_rotate(s)
                        s = x.parent.right
                    # Case 4
                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left  # Sibling node
                if s.color == "RED":
                    # Mirror case 1
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == "BLACK" and s.left.color == "BLACK":
                    # Mirror case 2
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.left.color == "BLACK":
                        # Mirror case 3
                        s.right.color = "BLACK"
                        s.color = "RED"
                        self.left_rotate(s)
                        s = x.parent.left
                    # Mirror case 4
                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"

    # Left rotate the subtree rooted at x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NULL_LEAF:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Right rotate the subtree rooted at x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NULL_LEAF:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Helper method for inorder traversal
    def inorder_helper(self, node, result):
        if node != self.NULL_LEAF:
            self.inorder_helper(node.left, result)
            result.append((node.key, node.value))
            self.inorder_helper(node.right, result)

    # Inorder traversal of the tree
    def inorder(self):
        result = []
        self.inorder_helper(self.root, result)
        return result

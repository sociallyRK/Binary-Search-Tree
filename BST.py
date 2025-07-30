class Node:
    def __init__(self, value):
        # Initialize a new node with a value
        self.value = value        # The data stored in this node
        self.left = None          # Pointer to left child
        self.right = None         # Pointer to right child

class BinarySearchTree:
    def __init__(self):
        # Initialize the tree with an empty root
        self.root = None

    def insert(self, value):
        # Public method to insert a value into the BST

        def _insert(node):
            # Recursive helper to insert at the correct position
            if node is None:
                return Node(value)  # Create new node if spot is empty

            # Decide whether to go left, right, or do nothing
            key = self._get_direction(node, value)

            # Dispatch to the correct handler based on key
            return self.dispatch_insert()[key](node, value, _insert)

        # Start recursion from root and update root if it was None
        self.root = _insert(self.root)

    def search(self, value):
        # Public method to search for a value in the BST

        def _search(node):
            if node is None:
                return False  # Reached leaf — not found

            key = self._get_direction(node, value)
            return self.dispatch_search()[key](node, value, _search)

        return _search(self.root)

    def _get_direction(self, node, value):
        # Helper that decides which direction to go
        if value == node.value:
            return 'equal'
        elif value < node.value:
            return 'left'
        else:
            return 'right'

    # Dispatch map for insert operation
    def dispatch_insert(self):
        return {
            'equal': self._do_nothing_insert,  # Duplicate, do nothing
            'left': self._insert_left,         # Insert in left subtree
            'right': self._insert_right        # Insert in right subtree
        }

    # Dispatch map for search operation
    def dispatch_search(self):
        return {
            'equal': self._return_true,        # Value found
            'left': self._search_left,         # Search left subtree
            'right': self._search_right        # Search right subtree
        }

    # === Insert Handlers ===

    def _do_nothing_insert(self, node, value, recurse):
        # No duplicates allowed — return the node unchanged
        return node

    def _insert_left(self, node, value, recurse):
        # Recurse into the left child
        node.left = recurse(node.left)
        return node

    def _insert_right(self, node, value, recurse):
        # Recurse into the right child
        node.right = recurse(node.right)
        return node

    # === Search Handlers ===

    def _return_true(self, node, value, recurse):
        # Value matches — found!
        return True

    def _search_left(self, node, value, recurse):
        # Continue search in the left subtree
        return recurse(node.left)

    def _search_right(self, node, value, recurse):
        # Continue search in the right subtree
        return recurse(node.right)

    # === Optional: Preorder Traversal ===

    def preorder(self):
        # Print the tree in preorder: root → left → right
        def _preorder(node):
            if node:
                print(node.value, end=' ')
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)
        print()

class Node:
    def __init__(self, value):
        self.value = value        # Value stored in this node
        self.left = None          # Left child (smaller)
        self.right = None         # Right child (larger)

class BinarySearchTree:
    def __init__(self):
        self.root = None          # Root of the entire tree

    def insert(self, value):
        def _insert(node):
            if node is None:
                return Node(value)

            key = self._get_direction(node, value)
            return self.dispatch_insert()[key](node, value, _insert)

        self.root = _insert(self.root)

    def search(self, value):
        def _search(node):
            if node is None:
                return False

            key = self._get_direction(node, value)
            return self.dispatch_search()[key](node, value, _search)

        return _search(self.root)

    def _get_direction(self, node, value):
        if value == node.value:
            return 'equal'
        elif value < node.value:
            return 'left'
        else:
            return 'right'

    # Dispatch maps — no lambdas
    def dispatch_insert(self):
        return {
            'equal': self._do_nothing_insert,
            'left': self._insert_left,
            'right': self._insert_right,
        }

    def dispatch_search(self):
        return {
            'equal': self._return_true,
            'left': self._search_left,
            'right': self._search_right,
        }

    # Insert Handlers
    def _do_nothing_insert(self, node, value, recurse): return node
    def _insert_left(self, node, value, recurse):
        node.left = recurse(node.left)
        return node
    def _insert_right(self, node, value, recurse):
        node.right = recurse(node.right)
        return node

    # Search Handlers
    def _return_true(self, node, value, recurse): return True
    def _search_left(self, node, value, recurse): return recurse(node.left)
    def _search_right(self, node, value, recurse): return recurse(node.right)

    def preorder(self):
        def _preorder(node):
            if node:
                print(node.value, end=' ')
                _preorder(node.left)
                _preorder(node.right)
        _preorder(self.root)
        print()

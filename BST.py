import inspect

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        # Detect external call: only warn if not called from inside this class
        caller_frame = inspect.stack()[1]
        caller_self = caller_frame.frame.f_locals.get('self')
        if not isinstance(caller_self, BinarySearchTree):
            print(f"⚠️ _insert called from outside the class (via '{caller_frame.function}')")

        if node is None:
            return Node(value)

        key = self._get_direction(node, value)
        handlers = self.dispatch_insert()
        return handlers[key](node, value)

    def _get_direction(self, node, value):
        if value < node.value:
            return 'left'
        elif value > node.value:
            return 'right'
        else:
            return 'none'

    def dispatch_insert(self):
        return {
            'left': self.handle_left_insert,
            'right': self.handle_right_insert,
            'none': self.handle_duplicate_insert
        }

    def handle_left_insert(self, node, value):
        node.left = self._insert(node.left, value)
        return node

    def handle_right_insert(self, node, value):
        node.right = self._insert(node.right, value)
        return node

    def handle_duplicate_insert(self, node, value):
        return node

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

# -----------------------
# ✅ Sample Test Cases
# -----------------------

if __name__ == "__main__":
    bst = BinarySearchTree()

    print("Inserting values: 1, 2, 3, 4, 5, 6, 7")
    for v in [1, 2, 3, 4, 5, 6, 7, 8]:
        bst.insert(v)

    print("\nSearch for existing values:")
    for v in [0, 1, 5]:
        print(f"search({v}) → {bst.search(v)}")

    print("\nSearch for non-existing values:")
    for v in [10, 5, 100]:
        print(f"search({v}) → {bst.search(v)}")

    print("\nDirect external call to _insert (should trigger warning):")
    bst._insert(None, 9)

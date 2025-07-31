import inspect

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    # Public insert
    def insert(self, value):
        self.root = self._insert(self.root, value)

    # Internal insert
    def _insert(self, node, value):
        caller_frame = inspect.stack()[1]
        caller_self = caller_frame.frame.f_locals.get('self')
        if not isinstance(caller_self, BinarySearchTree):
            print(f"⚠️ _insert called from outside the class (via '{caller_frame.function}')")

        if node is None:
            return Node(value)

        key = self._get_direction(node, value)
        handlers = self.dispatch_insert()
        return handlers[key](node, value)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        caller_frame = inspect.stack()[1]
        caller_self = caller_frame.frame.f_locals.get('self')
        if not isinstance(caller_self, BinarySearchTree):
            print(f"⚠️ _delete called from outside the class (via '{caller_frame.function}')")

        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._min_value_node(node.right)
                node.value = successor.value
                node.right = self._delete(node.right, successor.value)

        return node

    def _min_value_node(self, node):
        while node.left is not None:
            node = node.left
        return node

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

    def _print_node(self, node):
        print(node.value)

    def traverse(self, order):
        if order in ("in", "pre", "post"):
            self._traverse_recursive(self.root, order)
        elif order == "level":
            self._traverse_level_order()
        else:
            print(f"Unknown traversal order: {order}")

    def _traverse_recursive(self, node, order):
        if node is None:
            return
        if order == 'pre':
            self._print_node(node)
        self._traverse_recursive(node.left, order)
        if order == 'in':
            self._print_node(node)
        self._traverse_recursive(node.right, order)
        if order == 'post':
            self._print_node(node)

    def _traverse_level_order(self):
        if not self.root:
            return
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            self._print_node(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def traverseInOrder(self):
        self.traverse("in")

    def traversePreOrder(self):
        self.traverse("pre")

    def traversePostOrder(self):
        self.traverse("post")

    def traverseLevelOrder(self):
        self.traverse("level")


# -----------------------
# ✅ Test Cases
# -----------------------

if __name__ == "__main__":
    bst = BinarySearchTree()

    print("Inserting values: 1 to 8")
    for v in range(1, 9):
        bst.insert(v)

    print("\nSearch for existing values:")
    for v in [1, 4, 7]:
        print(f"search({v}) → {bst.search(v)}")

    print("\nSearch for non-existing values:")
    for v in [0, 10]:
        print(f"search({v}) → {bst.search(v)}")

    print("\nTraverse InOrder:")
    bst.traverseInOrder()

    print("\nTraverse PreOrder:")
    bst.traversePreOrder()

    print("\nTraverse PostOrder:")
    bst.traversePostOrder()

    print("\nTraverse LevelOrder:")
    bst.traverseLevelOrder()

    print("\nDeleting a leaf node (8):")
    bst.delete(8)
    bst.traverseLevelOrder()

    print("\nExternal access test:")
    bst._insert(None, 1000)
    bst._delete(None, 2000)

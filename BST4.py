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
        if node is None:
            return Node(value)

        key = self._get_direction(node, value)
        return self.dispatch_insert()[key](node, value)

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
        return node  # Do nothing for duplicates

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            successor = self._min_value_node(node.right)
            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        return node

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

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

        def pre_order():
            self._print_node(node)
            self._traverse_recursive(node.left, order)
            self._traverse_recursive(node.right, order)

        def in_order():
            self._traverse_recursive(node.left, order)
            self._print_node(node)
            self._traverse_recursive(node.right, order)

        def post_order():
            self._traverse_recursive(node.left, order)
            self._traverse_recursive(node.right, order)
            self._print_node(node)

        dispatch = {
            'pre': pre_order,
            'in': in_order,
            'post': post_order
        }

        dispatch[order]()

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

    def findMinimum(self):
        current = self.root
        while current and current.left:
            current = current.left
        return current.value if current else None

    def findMaximum(self):
        current = self.root
        while current and current.right:
            current = current.right
        return current.value if current else None

    def find(self, order, tracker_func, state):
        self._traverse_with_tracker(self.root, order, tracker_func, state)

    def _traverse_with_tracker(self, node, order, tracker_func, state):
        if node is None:
            return

        def pre_order():
            tracker_func(node, state)
            self._traverse_with_tracker(node.left, order, tracker_func, state)
            self._traverse_with_tracker(node.right, order, tracker_func, state)

        def in_order():
            self._traverse_with_tracker(node.left, order, tracker_func, state)
            tracker_func(node, state)
            self._traverse_with_tracker(node.right, order, tracker_func, state)

        def post_order():
            self._traverse_with_tracker(node.left, order, tracker_func, state)
            self._traverse_with_tracker(node.right, order, tracker_func, state)
            tracker_func(node, state)

        dispatch = {
            'pre': pre_order,
            'in': in_order,
            'post': post_order
        }

        dispatch[order]()

    def findSmallest(self, k):
        state = {'count': 0, 'kth': None}

        def track_kth(node, state):
            state['count'] += 1
            if state['count'] == k:
                state['kth'] = node.value

        self.find('in', track_kth, state)
        return state['kth']

    def sumSmaller(self, k):
        state = {'count': 0, 'sum': 0}

        def track_sum(node, state):
            if state['count'] < k:
                state['sum'] += node.value
                state['count'] += 1

        self.find('in', track_sum, state)
        return state['sum']


# -----------------------
# ✅ Test Cases
# -----------------------

if __name__ == "__main__":
    bst = BinarySearchTree()

    for v in [5, 3, 7, 2, 4, 6, 8, 1]:
        bst.insert(v)

    print("\nInOrder:")
    bst.traverseInOrder()

    print("\nPreOrder:")
    bst.traversePreOrder()

    print("\nPostOrder:")
    bst.traversePostOrder()

    print("\nLevelOrder:")
    bst.traverseLevelOrder()

    print("\nMinimum:", bst.findMinimum())
    print("Maximum:", bst.findMaximum())
    print("3rd Smallest:", bst.findSmallest(3))
    print("Sum of first 5 smallest:", bst.sumSmaller(5))

    print("\nDeleting 3 and 7:")
    bst.delete(3)
    bst.delete(7)

    print("\nInOrder After Deletion:")
    bst.traverseInOrder()

class Node:
    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None

    def __str__(self):
        left_str = "None"
        right_str = "None"

        if self.left is not None:
            left_str = str(self.left)

        if self.right is not None:
            right_str = str(self.right)

        return "(" + str(self.value) + " " + left_str + " " + right_str + ")"


class BinarySearchTree:
    def __init__(self):
        self._root = None

    def insert(self, value):
        self._root = self._insert_rec(self._root, value)

    def _insert_rec(self, node, value):
        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._insert_rec(node.left, value)
        else:
            node.right = self._insert_rec(node.right, value)

        return node

    def __str__(self):
        if self._root is None:
            return ""
        return str(self._root)


def preorder_to_bst(preorder):
    if preorder == []:
        return ""

    bst = BinarySearchTree()

    def add_all(lst, idx):
        if idx == len(lst):
            return
        bst.insert(lst[idx])
        add_all(lst, idx + 1)

    add_all(preorder, 0)
    return bst


#test
#print(preorder_to_bst([3, 2, 5]))
#preorder_to_bst([3])
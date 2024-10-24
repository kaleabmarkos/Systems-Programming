class TreeNode:
    def __init__(self, opcode, value, format):
        self.opcode = opcode
        self.value = value
        self.format = format
        self.left = None
        self.right = None


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, opcode, value, format):
        new_node = TreeNode(opcode, value, format)
        if self.root is None:
            self.root = new_node
        else:
            self._insert(self.root, new_node)

    def _insert(self, root, new_node):
        if new_node.opcode < root.opcode:
            if root.left is None:
                root.left = new_node
            else:
                self._insert(root.left, new_node)
        elif new_node.opcode > root.opcode:
            if root.right is None:
                root.right = new_node
            else:
                self._insert(root.right, new_node)
        else:
            print(f"ERROR - opcode previously defined: {root.opcode} (+)")

    def search(self, opcode):
        return self._search(self.root, opcode)

    def _search(self, root, opcode):
        if root is None:
            return None
        if opcode == root.opcode:
            return root
        elif opcode < root.opcode:
            return self._search(root.left, opcode)
        else:
            return self._search(root.right)

    def inorder_traversal(self, node, opcodes=[]):
        if node:
            self.inorder_traversal(node.left, opcodes)
            opcodes.append(node)
            self.inorder_traversal(node.right, opcodes)
        return opcodes

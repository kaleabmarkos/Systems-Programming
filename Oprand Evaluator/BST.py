class TreeNode:
    def __init__(self, symbol, value, rflag, iflag, mflag):
        self.symbol = symbol
        self.value = value
        self.rflag = rflag
        self.iflag = iflag
        self.mflag = mflag
        self.left = None
        self.right = None


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, symbol, value, rflag, iflag, mflag):
        new_node = TreeNode(symbol, value, rflag, iflag, mflag)
        if self.root is None:
            self.root = new_node
        else:
            self._insert(self.root, new_node)

  
    def _insert(self, root, new_node):
        if new_node.symbol < root.symbol:
            if root.left is None:
                root.left = new_node
            else:
                self._insert(root.left, new_node)
        elif new_node.symbol > root.symbol:
            if root.right is None:
                root.right = new_node
            else:
                self._insert(root.right, new_node)
        else:
            # Duplicate symbol - update MFLAG
            root.mflag = True
            print(f"ERROR - symbol previously defined: {root.symbol} (+)")
    
   

    def search(self, symbol):
        return self._search(self.root, symbol)


    def _search(self, root, symbol):
        if root is None:
            return None
        if symbol == root.symbol:
            return root
        elif symbol < root.symbol:
            return self._search(root.left, symbol)
        else:
            return self._search(root.right, symbol)
        

    def inorder_traversal(self, node, symbols=[]):
        if node:
            self.inorder_traversal(node.left, symbols)
            symbols.append(node)
            self.inorder_traversal(node.right, symbols)
        return symbols
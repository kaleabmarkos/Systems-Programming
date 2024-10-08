'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** CLASS : TreeNode
*********************************************************************
*** DESCRIPTION : The TreeNode class represents a node in a binary 
*** search tree (BST). Each node stores a symbol and its associated 
*** attributes (value, rflag, iflag, mflag), and has pointers to 
*** its left and right children. The class is used to construct 
*** the symbol table for the SIC/XE assembler, where each symbol 
*** is represented as a node in the tree.
*********************************************************************
*** INPUT ARGS : symbol (string) - the symbol being inserted into 
***              the tree (first 4 characters are significant)
***              value (int) - the integer value associated with 
***              the symbol
***              rflag (bool) - the relocation flag (true or false)
***              iflag (bool) - indicates if the symbol is defined 
***              in the current control section (true for now)
***              mflag (bool) - indicates if the symbol is 
***              multiply defined (starts as false)
*** OUTPUT ARGS : None
*** IN/OUT ARGS : None
*** RETURN : Returns an instance of the TreeNode class, which has 
*** left and right child pointers, and stores the provided symbol 
*** and its attributes (value, rflag, iflag, mflag).
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class TreeNode:
    def __init__(self, symbol, value, rflag, iflag, mflag):
        self.symbol = symbol
        self.value = value
        self.rflag = rflag
        self.iflag = iflag
        self.mflag = mflag
        self.left = None
        self.right = None

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** CLASS : BinarySearchTree
*********************************************************************
*** DESCRIPTION : The BinarySearchTree class implements a binary 
*** search tree (BST) to manage the symbol table for the SIC/XE assembler. 
*** It allows the insertion of symbols, searching for symbols, and 
*** traversing the tree in order. Each symbol is stored in a TreeNode 
*** with its associated attributes (value, rflag, iflag, mflag), and the 
*** class ensures that the tree maintains its binary search property, 
*** where left children are smaller and right children are larger 
*** than the parent node.
*********************************************************************
*** INPUT ARGS : None (the class methods will handle input as needed)
*** OUTPUT ARGS : None
*** IN/OUT ARGS : root (TreeNode) - represents the root node of 
***               the binary search tree, updated with each insertion
*** RETURN : Returns an instance of the BinarySearchTree class, which 
*** contains methods for inserting nodes, searching for symbols, and 
*** performing an inorder traversal of the tree.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class BinarySearchTree:

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: Constructor (__init__) ***
    *********************************************************************
    *** DESCRIPTION : This is the constructor for the BinarySearchTree class.
    *** It initializes the binary search tree by setting the root node 
    *** to None, representing an empty tree at the beginning.
    *** INPUT ARGS : None
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def __init__(self):
        self.root = None

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: insert ***
    *********************************************************************
    *** DESCRIPTION : This function inserts a new symbol into the binary 
    *** search tree. It creates a new TreeNode object with the given 
    *** symbol and attributes (value, rflag, iflag, mflag) and inserts 
    *** it in the appropriate location in the tree based on the 
    *** binary search property.
    *** INPUT ARGS : symbol (string) - the symbol to be inserted 
    ***              value (int) - the integer value associated with the symbol
    ***              rflag (bool) - relocation flag (true or false)
    ***              iflag (bool) - flag indicating if the symbol is defined 
    ***              in the current control section (true for now)
    ***              mflag (bool) - flag indicating if the symbol has been 
    ***              multiply defined (starts as false)
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : root (TreeNode) - the root node of the binary search tree
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def insert(self, symbol, value, rflag, iflag, mflag):
        new_node = TreeNode(symbol, value, rflag, iflag, mflag)
        if self.root is None:
            self.root = new_node
        else:
            self._insert(self.root, new_node)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: _insert ***
    *********************************************************************
    *** DESCRIPTION : This is a helper function for the insert method. It 
    *** recursively finds the correct position for the new node in the 
    *** binary search tree by comparing the new symbol with the current 
    *** root node. If the symbol already exists, it sets the MFLAG to true 
    *** and prints an error message indicating that the symbol has been 
    *** previously defined.
    *** INPUT ARGS : root (TreeNode) - the current node in the binary search tree
    ***              new_node (TreeNode) - the node to be inserted into the tree
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  
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
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: search ***
    *********************************************************************
    *** DESCRIPTION : This function searches for a symbol in the binary search tree. 
    *** It calls the helper method _search to locate the symbol in the tree. 
    *** If the symbol is found, the corresponding TreeNode is returned; 
    *** otherwise, None is returned.
    *** INPUT ARGS : symbol (string) - the symbol to search for in the tree
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : (TreeNode or None) - returns the node if the symbol is found,
    *** otherwise returns None.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def search(self, symbol):
        return self._search(self.root, symbol)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: _search ***
    *********************************************************************
    *** DESCRIPTION : This is a helper function for the search method. 
    *** It recursively searches for a symbol in the binary search tree, 
    *** comparing the symbol with the current root node and traversing 
    *** the left or right subtree accordingly.
    *** INPUT ARGS : root (TreeNode) - the current node in the binary search tree
    ***              symbol (string) - the symbol to search for
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : (TreeNode or None) - returns the node if the symbol is found,
    *** otherwise returns None.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def _search(self, root, symbol):
        if root is None:
            return None
        if symbol == root.symbol:
            return root
        elif symbol < root.symbol:
            return self._search(root.left, symbol)
        else:
            return self._search(root.right, symbol)
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: inorder_traversal ***
    *********************************************************************
    *** DESCRIPTION : This function performs an inorder traversal of the binary 
    *** search tree and appends each visited node to a list. The inorder 
    *** traversal visits nodes in ascending order based on their symbol.
    *** INPUT ARGS : node (TreeNode) - the current node to traverse
    ***              symbols (list) - a list to store nodes during traversal
    *** OUTPUT ARGS : symbols (list) - updated list of nodes visited in order
    *** IN/OUT ARGS : symbols (list) - modified as nodes are visited
    *** RETURN : (list) - returns the list of nodes visited during inorder traversal.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''       

    def inorder_traversal(self, node, symbols=[]):
        if node:
            self.inorder_traversal(node.left, symbols)
            symbols.append(node)
            self.inorder_traversal(node.right, symbols)
        return symbols
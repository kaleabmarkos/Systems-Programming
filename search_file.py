'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** NAME : Kaleab Gessese
*** CLASS : CSc 354
*** ASSIGNMENT : 01
*** DUE DATE : 09/18/2024
*** INSTRUCTOR : HAMER 
*********************************************************************
*** DESCRIPTION : This project implements a symbol table for the SIC/XE 
            assembler using a binary search tree (BST). It reads symbols 
            from a file, validates them based on specific rules (symbols 
            must start with a letter, be at most 10 characters long, and 
            contain only letters, digits, or underscores), and inserts valid
            symbols into the tree. Duplicate symbols are handled by setting
            a "multiple definition flag" (MFLAG) to true and displaying an 
            error message. Additionally, the program allows searching for 
            symbols and displays an error if a symbol is invalid or not found. 
            The symbol table can also be traversed in order to display all symbols 
            and their attributes.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


import sys
import re

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
    

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** CLASS: SymbolTable ***
*********************************************************************
*** DESCRIPTION : The SymbolTable class manages the symbol table using 
*** a Binary Search Tree (BST) for efficient insertion, searching, and 
*** traversal of symbols. The class handles the validation of symbols, 
*** their values, and associated flags (rflag, iflag, mflag). It provides 
*** methods to load symbols from a file, insert valid symbols into the BST, 
*** search for symbols, and display the entire symbol table in a formatted 
*** output.
*** INPUT ARGS : None (class methods accept input arguments as needed)
*** OUTPUT ARGS : None (class methods output data as needed)
*** IN/OUT ARGS : bst (BinarySearchTree) - stores the root of the binary 
*** search tree, which is updated with each symbol insertion.
*** RETURN : Returns an instance of the SymbolTable class, which contains 
*** methods for validating symbols, inserting them into the tree, 
*** searching, and displaying symbols.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class SymbolTable:
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: Constructor (__init__) ***
    *********************************************************************
    *** DESCRIPTION : This is the constructor for the SymbolTable class. 
    *** It initializes the class by creating an instance of the 
    *** BinarySearchTree, which will be used to store and manage the symbols.
    *** INPUT ARGS : None
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def __init__(self):
        self.bst = BinarySearchTree()
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: validate_symbol_format ***
    *********************************************************************
    *** DESCRIPTION : This function validates the format of a given symbol. 
    *** It checks if the symbol starts with a letter, is at most 10 characters 
    *** long, and contains only valid characters (letters, digits, and underscores). 
    *** If any of these conditions are not met, an appropriate error message 
    *** is returned.
    *** INPUT ARGS : symbol (string) - the symbol to validate
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : (bool, string) - returns True and None if the symbol is valid, 
    *** otherwise returns False and an error message.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def validate_symbol_format(self, symbol):
        # Check if symbol starts with a letter
        if not symbol[0].isalpha():
            return False, "ERROR - symbols start with a letter: " + symbol

        # Check if the symbol is within the valid length (1 to 10 characters)
        if len(symbol) > 10:
            return False, "ERROR - symbols contain 10 characters maximum: " + symbol

        # Check if symbol starts with a letter, max length 10 (excluding colon)
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]{0,10}$", symbol):
            return False, "ERROR - symbols contain letters, digits and underscore: " + symbol
        return True, None
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: validate_value ***
    *********************************************************************
    *** DESCRIPTION : This function validates the value of a symbol. It checks 
    *** if the value is a valid signed integer. If the value is invalid, 
    *** an error message is returned.
    *** INPUT ARGS : value (string) - the value associated with the symbol
    ***              symbol (string) - the symbol associated with the value
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : (bool, int, string) - returns True and the integer value if valid, 
    *** otherwise returns False and an error message.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def validate_value(self, value, symbol):
        # Check if value is a valid signed integer
        try:
            int_value = int(value)
            return True, int_value, None
        except ValueError:
            return False, None, f"ERROR - symbol {symbol} invalid value: {value}"

    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: validate_rflag ***
    *********************************************************************
    *** DESCRIPTION : This function validates the rflag associated with a symbol. 
    *** It checks if the rflag is either "true" or "false". If the rflag is invalid, 
    *** an error message is returned.
    *** INPUT ARGS : rflag (string) - the rflag value associated with the symbol
    ***              symbol (string) - the symbol associated with the rflag
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : (bool, int, string) - returns True and the boolean value (1 or 0) 
    *** if valid, otherwise returns False and an error message.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def validate_rflag(self, rflag, symbol):
        # Check if RFLAG is a valid boolean (true/false)
        rflag = rflag.lower()
        if rflag in ["true", "false"]:
            return True, 1 if rflag == "true" else 0, None
        else:
            return False, None, f"ERROR - symbol {symbol} invalid rflag: {rflag}"
    
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: insert_symbol ***
    *********************************************************************
    *** DESCRIPTION : This function inserts a valid symbol into the symbol table. 
    *** It first validates the symbol, value, and rflag before inserting the symbol 
    *** into the binary search tree with the associated attributes (value, rflag, iflag, mflag).
    *** INPUT ARGS : symbol (string) - the symbol to insert
    ***              value (string) - the value associated with the symbol
    ***              rflag (string) - the rflag value associated with the symbol
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def insert_symbol(self, symbol, value, rflag):
        # Insert valid symbols into the symbol table
        check, note = self.validate_symbol_format(symbol)
        if not check:
            print(note)
            return
        
        symbol_key = symbol[:4]  # Only the first 4 characters are significant

        is_valid_value, int_value, value_error = self.validate_value(value, symbol_key)
        if not is_valid_value:
            print(value_error)
            return

        is_valid_rflag, bool_rflag, rflag_error = self.validate_rflag(rflag, symbol_key)
        if not is_valid_rflag:
            print(rflag_error)
            return

        # Insert the symbol and its attributes into the symbol table
        symbol_keyy = symbol[:4].upper()
        iflag = True  # Set IFLAG to True for now
        mflag = False # Set MFLAG initially to False
        self.bst.insert(symbol_keyy, int_value, bool_rflag, iflag, mflag)
    
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: load_symbols ***
    *********************************************************************
    *** DESCRIPTION : This function loads symbols from a given file. 
    *** It reads each line of the file, splits the line into symbol, value, 
    *** and rflag, and inserts each valid symbol into the symbol table.
    *** INPUT ARGS : filename (string) - the name of the file to load symbols from
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



    def load_symbols(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) != 3:
                    print(f"ERROR - invalid line format: {line.strip()}")
                    continue
                
                symbol = parts[0].rstrip(":")
                value = parts[1]
                rflag = parts[2]
                
                self.insert_symbol(symbol, value, rflag)
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: search_symbol ***
    *********************************************************************
    *** DESCRIPTION : This function searches for a symbol in the symbol table. 
    *** It first validates the symbol format and then searches for the symbol 
    *** in the binary search tree. If the symbol is found, its attributes are displayed. 
    *** Otherwise, an error message is printed.
    *** INPUT ARGS : symbol (string) - the symbol to search for
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def search_symbol(self, symbol):
        
        # Validate the symbol format before searching
        check, note = self.validate_symbol_format(symbol)
        if not check:
            print(note)
            return
        
        # If valid, perform the search
        symbol_key = symbol[:4].upper()  # Only the first 4 characters are significant
        node = self.bst.search(symbol_key)
        
        if node:
            print(f"FOUND - Symbol: {node.symbol}, Value: {node.value}, RFlag: {node.rflag}, IFlag: {node.iflag}, MFlag: {node.mflag}")
        else:
            print(f"ERROR - {symbol} not found in the symbol table")
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: display_symbols ***
    *********************************************************************
    *** DESCRIPTION : This function displays all symbols in the symbol table 
    *** in tabular format. It performs an inorder traversal of the binary 
    *** search tree and prints the symbol, value, rflag, iflag, and mflag 
    *** for each node in the tree.
    *** INPUT ARGS : None
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


    def display_symbols(self):
        symbols = self.bst.inorder_traversal(self.bst.root)
        print(f"\n{'Symbol':<10} {'Value':<10} {'RFlag':<6} {'IFlag':<6} {'MFlag':<6}\n")
        for symbol in symbols:
            print(f"{symbol.symbol:<10} {symbol.value:<10} {symbol.rflag:<6} {symbol.iflag:<6} {symbol.mflag:<6}")
    

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** FUNCTION: main ***
*********************************************************************
*** DESCRIPTION : The main function serves as the entry point for the 
*** program. It creates an instance of the SymbolTable class, loads symbols 
*** from the "SYMS.DAT" file, and searches for symbols based on the input 
*** from a second file or user input. It also displays the contents of the 
*** symbol table in a formatted table after processing all the symbols.
*** INPUT ARGS : None (the function interacts with external files and 
*** command-line arguments for input)
*** OUTPUT ARGS : None (the function outputs search results and the symbol 
*** table to the console)
*** IN/OUT ARGS : symbol_table (SymbolTable) - instance of the SymbolTable 
*** class that manages the symbol insertion, search, and display processes.
*** RETURN : None (the function doesn't return any value, it handles 
*** file processing and output display)
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



def main():
    symbol_table = SymbolTable()

    # Step 1: Load symbols from SYMS.DAT
    print()
    symbol_table.load_symbols("SYMS.DAT")

    # Step 2: Read search file and process symbols
    if len(sys.argv) > 1:
        search_file = sys.argv[1]
    else:
        search_file = input("\nEnter the search file name: ")
        print()

    try:
        with open(search_file, 'r') as file:
            for line in file:
                symbol = line.strip()
                if symbol:
                    symbol_table.search_symbol(symbol)
    except FileNotFoundError:
        print(f"\nERROR - search file {search_file} not found\n")
    
    # Step 3: Display the symbol table
    symbol_table.display_symbols()

if __name__ == "__main__":
    main()

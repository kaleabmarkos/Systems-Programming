'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** NAME : Kaleab Gessese
*** CLASS : CSc 354
*** ASSIGNMENT : 01
*** DUE DATE : 09/18/2024
*** INSTRUCTOR : HAMER 
*********************************************************************
*** DESCRIPTION : 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


import sys
import re

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** FUNCTION <name of function> ***
*********************************************************************
*** DESCRIPTION : <detailed english description of the function> ***
*** INPUT ARGS : <list of all input argument names> ***
*** OUTPUT ARGS : <list of all output argument names> ***
*** IN/OUT ARGS : <list of all input/output argument names> ***
*** RETURN : <return type and return value name> ***
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
*** FUNCTION <name of function> ***
*********************************************************************
*** DESCRIPTION : <detailed english description of the function> ***
*** INPUT ARGS : <list of all input argument names> ***
*** OUTPUT ARGS : <list of all output argument names> ***
*** IN/OUT ARGS : <list of all input/output argument names> ***
*** RETURN : <return type and return value name> ***
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class BinarySearchTree:
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def __init__(self):
        self.root = None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def insert(self, symbol, value, rflag, iflag, mflag):
        new_node = TreeNode(symbol, value, rflag, iflag, mflag)
        if self.root is None:
            self.root = new_node
        else:
            self._insert(self.root, new_node)
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
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
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def search(self, symbol):
        return self._search(self.root, symbol)
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
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
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def inorder_traversal(self, node, symbols=[]):
        if node:
            self.inorder_traversal(node.left, symbols)
            symbols.append(node)
            self.inorder_traversal(node.right, symbols)
        return symbols
    

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** FUNCTION <name of function> ***
*********************************************************************
*** DESCRIPTION : <detailed english description of the function> ***
*** INPUT ARGS : <list of all input argument names> ***
*** OUTPUT ARGS : <list of all output argument names> ***
*** IN/OUT ARGS : <list of all input/output argument names> ***
*** RETURN : <return type and return value name> ***
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class SymbolTable:
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def __init__(self):
        self.bst = BinarySearchTree()
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
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
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def validate_value(self, value, symbol):
        # Check if value is a valid signed integer
        try:
            int_value = int(value)
            return True, int_value, None
        except ValueError:
            return False, None, f"ERROR - symbol {symbol} invalid value: {value}"
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def validate_rflag(self, rflag, symbol):
        # Check if RFLAG is a valid boolean (true/false)
        rflag = rflag.lower()
        if rflag in ["true", "false"]:
            return True, 1 if rflag == "true" else 0, None
        else:
            return False, None, f"ERROR - symbol {symbol} invalid rflag: {rflag}"
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
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
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
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
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def search_symbol(self, symbol):
        # symbol_key = symbol[:4].upper()
        # node = self.bst.search(symbol_key)
        # if node:
        #     print(f"Symbol: {node.symbol}, Value: {node.value}, RFlag: {node.rflag}, IFlag: {node.iflag}, MFlag: {node.mflag}")
        # else:
        #     print(f"ERROR - symbol {symbol} not found")

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
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def display_symbols(self):
        symbols = self.bst.inorder_traversal(self.bst.root)
        print(f"\n{'Symbol':<10} {'Value':<10} {'RFlag':<6} {'IFlag':<6} {'MFlag':<6}\n")
        for symbol in symbols:
            print(f"{symbol.symbol:<10} {symbol.value:<10} {symbol.rflag:<6} {symbol.iflag:<6} {symbol.mflag:<6}")
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION <name of function> ***
    *********************************************************************
    *** DESCRIPTION : <detailed english description of the function> ***
    *** INPUT ARGS : <list of all input argument names> ***
    *** OUTPUT ARGS : <list of all output argument names> ***
    *** IN/OUT ARGS : <list of all input/output argument names> ***
    *** RETURN : <return type and return value name> ***
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

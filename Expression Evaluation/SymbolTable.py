from BST import BinarySearchTree
import re

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
        

        is_valid_value, int_value, value_error = self.validate_value(value, symbol)
        if not is_valid_value:
            print(value_error)
            return

        is_valid_rflag, bool_rflag, rflag_error = self.validate_rflag(rflag, symbol)
        if not is_valid_rflag:
            print(rflag_error)
            return

        # Insert the symbol and its attributes into the symbol table
        symbol_keyy = symbol.upper()
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
            return None

        # Perform the search in the BST
        symbol_key = symbol.upper()  # Convert symbol to uppercase for uniformity
        return self.bst.search(symbol_key)
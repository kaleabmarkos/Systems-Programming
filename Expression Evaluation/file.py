from BST import BinarySearchTree
import sys, re
import sys
from BST import BinarySearchTree  # Assuming BST is implemented in this module
from Expressions import ExpressionVerifier
class SymbolTable:
    
    def __init__(self):
        self.bst = BinarySearchTree()
    

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
    

    def validate_value(self, value, symbol):
        # Check if value is a valid signed integer
        try:
            int_value = int(value)
            return True, int_value, None
        except ValueError:
            return False, None, f"ERROR - symbol {symbol} invalid value: {value}"

    

    def validate_rflag(self, rflag, symbol):
        # Check if RFLAG is a valid boolean (true/false)
        rflag = rflag.lower()
        if rflag in ["true", "false"]:
            return True, 1 if rflag == "true" else 0, None
        else:
            return False, None, f"ERROR - symbol {symbol} invalid rflag: {rflag}"
    
    

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
    
    def search_symbol(self, symbol):
        # Validate the symbol format before searching
        check, note = self.validate_symbol_format(symbol)
        if not check:
            print(note)
            return None

        # Perform the search in the BST
        symbol_key = symbol.upper()  # Convert symbol to uppercase for uniformity
        return self.bst.search(symbol_key)



def main():
    # Initialize Symbol Table and Expression Verifier
    symbol_table = SymbolTable()

    # Load symbols from SYMS.DAT
    symbol_table.load_symbols('SYMS.DAT')  # Ensure SYMS.DAT file exists

    # Initialize the expression verifier with the loaded symbol table
    ev = ExpressionVerifier(symbol_table)

    # Check if an expression file is provided through command line or prompt for input
    if len(sys.argv) > 1:
        search_file = sys.argv[1]
    else:
        search_file = input("\nEnter the expression file name: ")
        print()

    try:
        # Read expressions from the input file
        with open(search_file, 'r') as file:
            for line in file:
                expression = line.strip()  # Strip leading/trailing spaces
                if expression:
                    ev.verify_expression(expression)  # Verify the expression

    except FileNotFoundError:
        print(f"\nERROR - expression file {search_file} not found\n")
        return

    # Display the verified expressions and literal table
    ev.display_expressions()
    ev.display_literals()


if __name__ == "__main__":
    main()
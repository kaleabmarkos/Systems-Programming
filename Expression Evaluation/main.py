'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** NAME : Kaleab Gessese
*********************************************************************
*** DESCRIPTION :  This project implements a module that evaluates the 
operand field of an assembly language statement for the SIC/XE assembler. 
It reads symbols and expressions from files, validates and processes them, 
and stores the results in a binary search tree (BST) for the symbol table
and a linked list for the literal table. It calculates the value, addressing mode,
and relocatability of the symbols and expressions. The module reads symbols and
their attributes from a file called SYMS.DAT and inserts them into a BST.
It also reads expressions from a file and evaluates them, supporting both
symbols and literals. Expressions may contain a combination of symbols,
immediate values, and indexed addressing. Addition and subtraction are the 
only allowed operations between symbols and numeric literals. Unique literals
are stored in a literal table with their value, length, and address. 
Expressions are displayed with their evaluated attributes, and literals 
are displayed in the literal table. The project ensures that all symbols 
are valid, addresses duplicate symbols, and handles the proper evaluation 
of different addressing modes, including indirect, immediate, and indexed 
addressing. Errors are printed for invalid expressions, and the content of
both the symbol and literal tables is displayed in a user-friendly format.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from Expressions import ExpressionVerifier
from SymbolTable import SymbolTable
import sys

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** FUNCTION: main ***
*********************************************************************
*** DESCRIPTION : The main function serves as the entry point for the program.
*** It initializes a symbol table and loads symbols from a file (SYMS.DAT),
*** then creates an expression verifier to process expressions from an input file.
*** The function verifies each expression and finally displays the evaluated
*** expressions and literals in formatted tables.
*********************************************************************
*** INPUT ARGS :
*** None - The function interacts with external files (SYMS.DAT and an expression file)
*** and can also take a command-line argument specifying the expression file.
*** OUTPUT ARGS :
*** None - Outputs the evaluated expressions and literals in formatted tables.
*** IN/OUT ARGS :
*** symbol_table (SymbolTable) - The symbol table instance that stores symbols from SYMS.DAT.
*** RETURN :
*** None - The function does not return any values.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

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
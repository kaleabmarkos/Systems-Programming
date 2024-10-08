'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** CLASS : Expression
*********************************************************************
*** DESCRIPTION : The Expression class represents an evaluated expression in the SIC/XE assembler.
*** Each expression stores the original expression string, its evaluated value,
*** relocatability status, and flags indicating whether the addressing mode uses
*** n-bit, i-bit, or x-bit (indirect, immediate, or indexed addressing).
*********************************************************************
*** INPUT ARGS : expression (str) - The expression string that is being evaluated.
***             ex_value (int) - The calculated value of the expression.
***             relocatable (str) - Indicates whether the expression is relocatable ("ABSOLUTE" or "RELATIVE").
***             n_bit (bool) - Indicates whether the expression uses n-bit (indirect addressing).
***             i_bit (bool) - Indicates whether the expression uses i-bit (immediate addressing).
***             x_bit (bool) - Indicates whether the expression uses x-bit (indexed addressing).
*** OUTPUT ARGS : None
*** IN/OUT ARGS : None
*** RETURN : Returns an instance of the Expression class containing the evaluated attributes of the expression.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class Expression:
    def __init__(self, expression, ex_value, relocatable, n_bit=False, i_bit=False, x_bit=False):
        self.expression = expression
        self.ex_value = ex_value
        self.relocatable = relocatable
        self.n_bit = n_bit
        self.i_bit = i_bit
        self.x_bit = x_bit

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** CLASS : Literal
*********************************************************************
*** DESCRIPTION : The Literal class represents a literal found in an expression in the SIC/XE assembler.
*** Each literal is stored with its name, calculated value, length, and assigned address.
*********************************************************************
*** INPUT ARGS : name (str) - The literal name, which includes the "=" sign and the character or hex value.
***             value (int/str) - The calculated value of the literal.
***             length (int) - The length of the literal in bytes.
***             address (int) - The memory address assigned to the literal.
*** OUTPUT ARGS : None
*** IN/OUT ARGS : None
*** RETURN : Returns an instance of the Literal class containing the attributes of the literal.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class Literal:
    def __init__(self, name, value, length, address):
        self.name = name
        self.value = value
        self.length = length
        self.address = address

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
*** CLASS : ExpressionVerifier
*********************************************************************
*** DESCRIPTION : The ExpressionVerifier class is responsible for evaluating and verifying expressions in
*** the SIC/XE assembler. It processes expressions, stores evaluated expressions,
*** and stores literals found during the evaluation. It can also handle arithmetic operations,
*** indirect and immediate addressing, and index-based addressing.
*********************************************************************
*** INPUT ARGS :
*** symbol_table (SymbolTable) - The symbol table that will be used for lookup during expression verification.
*** OUTPUT ARGS : None
*** IN/OUT ARGS : None
*** RETURN : Returns an instance of the ExpressionVerifier class that manages the verification process of expressions.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class ExpressionVerifier:

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: Constructor (init) ***
    *********************************************************************
    *** DESCRIPTION : This is the constructor for the ExpressionVerifier class.
    *** It initializes the symbol table reference, creates an empty list to hold expressions,
    *** and another to hold literals. It also sets the starting address counter for literals.
    *********************************************************************
    *** INPUT ARGS : symbol_table (SymbolTable) - Reference to the symbol table.
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.expressions = []
        self.literals = []
        self.literal_address_counter = 0

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: verify_expression ***
    *********************************************************************
    *** DESCRIPTION : This function verifies and evaluates an individual expression. It handles
    *** various addressing modes (indexed, immediate, and indirect), arithmetic operations
    *** (addition and subtraction), and evaluates literals if found. Errors are handled
    *** for invalid symbols or addressing mode conflicts.
    *********************************************************************
    *** INPUT ARGS : expression (str) - The expression to be evaluated.
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def verify_expression(self, expression):
        n_bit = i_bit = x_bit = False
        relocatable = "ABSOLUTE"
        value = None
        original_expression = expression.strip()

        # Check for special cases like @, #, and ,
        if expression.startswith('@'):
            if 'X' in expression or 'x' in expression:
                if len(expression) > 1 and expression[1].isdigit():
                    n_bit = i_bit = True
                else:
                    new_expression = Expression(f"{original_expression}", '-', '-', '-', '*', '* \t<- This is an error b/c X and N can\'t be 1')
                    self.expressions.append(new_expression)
                    return
            if len(expression) > 1 and expression[1].isdigit():
                n_bit = i_bit = True
            else:        
                expression = expression[1:]  # Remove '@'
                n_bit = True  # Set n-bit
        
        elif expression.startswith('#'):
            if 'X' in expression or 'x' in expression:
                if len(expression) > 1 and expression[1].isdigit():
                    n_bit = i_bit = True
                else:
                    new_expression = Expression(f"{original_expression}", '-', '-', '-', '*', '* \t<- This is an error b/c X and I can\'t be 1')
                    self.expressions.append(new_expression)
                    return
            if len(expression) > 1 and expression[1].isdigit():
                n_bit = i_bit = True
            else:
                expression = expression[1:]  # Remove '#'
                i_bit = True  # Set i-bit
        else:
            # If the symbol is standard (not @ or #), both n_bit and i_bit should be True
            n_bit = i_bit = True
            
        # Handle expressions starting with "=" to add to literal table
        if expression.startswith('='):
            literal_value, length = self.process_literal(expression)
            if literal_value == "-":
                self.literals.append(Literal(expression, '-', '-', '- \t <- Unsupported literal format'))
            elif literal_value and literal_value != '-':
                self.literals.append(Literal(expression, literal_value, length, self.literal_address_counter))
            return None  # Skipping as this goes to literal table
        
        # Check if the expression is purely numeric (like 22)
        if expression.isdigit():
            # Treat as an immediate value
            value = int(expression)
            i_bit = True  # Set the immediate addressing bit to true
            # Add the expression to the table (e.g., it would show as "#22")
            new_expression = Expression(f"#{expression}", value, relocatable, n_bit, i_bit, x_bit)
            self.expressions.append(new_expression)
            return  # Skip further processing since it's a valid numeric expression
                

        # Handling comma-based indexing
        if ',' in expression:
            expression, check = expression.split(',')
            if str(check).lower() == 'x':
                x_bit = True
        
        # Handle symbol lookup and value modification
        if '+' in expression:
            op1, op2 = map(str.strip, expression.split('+'))
            if op1[1:].isdigit():
                op1 = int(op1.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op2)
                value += op1  # Adding the number to the symbol's value
            elif op2[1:].isdigit():
                op2 = int(op2.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op1)
                value += op2  # Adding the number to the symbol's value
            else:
                val_of_op1, relocatable_of_op1 = self.lookup_symbol(op1)
                val_of_op2, relocatable_of_op2 = self.lookup_symbol(op2)
                if val_of_op1 and val_of_op2:
                    if (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "RELATIVE"):
                        relocatable = "RELATIVE"
                    elif (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "ABSOLUTE"):
                        relocatable = "ABSOLUTE"
                    elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "ABSOLUTE"):
                        relocatable = "RELATIVE"
                    elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "RELATIVE"):
                        relocatable = "RR"
                    
                    value = val_of_op1+val_of_op2

        elif '-' in expression:
            op1, op2 = map(str.strip, expression.split('-'))
            if op1[1:].isdigit():
                op1 = int(op1.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op2)
                value = op1 - value  # Subtracting the number from the symbol's value
            elif op2[1:].isdigit():
                op2 = int(op2.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op1)
                value -= op2  # Subtracting the number form the symbol's value
            else:
                val_of_op1, relocatable_of_op1 = self.lookup_symbol(op1)
                val_of_op2, relocatable_of_op2 = self.lookup_symbol(op2)
                if val_of_op1 and val_of_op2:
                    if (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "RELATIVE"):
                        relocatable = "AR"
                    elif (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "ABSOLUTE"):
                        relocatable = "ABSOLUTE"
                    elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "ABSOLUTE"):
                        relocatable = "RELATIVE"
                    elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "RELATIVE"):
                        relocatable = "ABSOLUTE"
                    
                    value = val_of_op1-val_of_op2
        else:
            value, relocatable = self.lookup_symbol(expression)

        if value and relocatable != "AR" and relocatable != "RR":
            # Add valid expression to the list
            new_expression = Expression(original_expression, value, relocatable, n_bit, i_bit, x_bit)
            self.expressions.append(new_expression)
        elif not value:
            new_expression = Expression(f"{original_expression}", '-', '-', '-', '-', f'- \t<- This is not applicable b/c {original_expression} is not in the symbol table')
            self.expressions.append(new_expression)
        elif relocatable == "AR":
            new_expression = Expression(f"{original_expression}", '-', '-', '-', '-', '- \t<- This is an error b/c the RFLAGs are False and True with the \'-\' operator')
            self.expressions.append(new_expression)
        elif relocatable == "RR":
            new_expression = Expression(f"{original_expression}", '-', '-', '-', '-', '- \t<- This is an error b/c the RFLAGs are True and True with the \'+\' operator')
            self.expressions.append(new_expression)
        

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: lookup_symbol ***
    *********************************************************************
    *** DESCRIPTION : This function looks up a symbol in the symbol table (BST). If found,
    *** it returns the value and relocatability status ("ABSOLUTE" or "RELATIVE") of the symbol.
    *** Otherwise, it returns an error message stating the symbol was not found.
    *********************************************************************
    *** INPUT ARGS : symbol (str) - The symbol to search for in the symbol table.
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : Returns the symbol's value and relocatability status, or an error if not found.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def lookup_symbol(self, symbol):
        # Use the symbol table to look up the symbol in the BST
        node = self.symbol_table.search_symbol(symbol.strip())
        if node:
            return node.value, "RELATIVE" if node.rflag else "ABSOLUTE"
        else:
            return None, f"Symbol {symbol} not found in the Symbol Table"
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: process_literal ***
    *********************************************************************
    *** DESCRIPTION : This function processes a literal found in an expression. It checks for
    *** whether the literal is a character or hexadecimal literal, calculates its value,
    *** and returns the literal's value and length. It also ensures duplicate literals
    *** are not stored more than once.
    *********************************************************************
    *** INPUT ARGS : literal (str) - The literal to be processed (must start with '=C' or '=X').
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : Returns the processed literal's value and its length.
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def process_literal(self, literal):

        # Check if the literal already exists
        for lit in self.literals:
            if lit.name == literal:
                return None,0  # If found, return the existing literal value
        length=0
        # If the first character is 'C', treat the following characters as ASCII
        if literal.startswith('=0C'):
            ascii_part = literal[3:]  # Skip the 'C'
            ascii_value = ''.join(str(hex(ord(char))[2:]) for char in ascii_part)  # Convert each character to its ASCII code
            literal_value = ascii_value
            length = len(literal[3:])
            self.literal_address_counter += 1
            
        elif literal.startswith('=0X'):
            hex_part = literal[3:]  # Skip the 'X'
            literal_value = hex_part  # Take the hexpart
            length = 1
            self.literal_address_counter += 1
        else:
            return '-', 0

        return literal_value, length    

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: display_expressions ***
    *********************************************************************
    *** DESCRIPTION : This function displays all evaluated expressions in a formatted table.
    *** It shows the expression, its value, relocatability status, and addressing mode flags.
    *********************************************************************
    *** INPUT ARGS : None
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def display_expressions(self):
        print()
        print("\t\t\tEXPRESSIONS")
        print("----------------------------------------------------------------------")
        print(f"{'EXPRESSION':<15} {'VALUE':<10} {'RELOCATABLE':<15} {'N-Bit':<10} {'I-Bit':<10} {'X-Bit':<10}")
        print("----------------------------------------------------------------------")        
        for exp in self.expressions:
            if isinstance(exp.n_bit, str) and exp.n_bit.isdigit() and isinstance(exp.i_bit, str) and exp.i_bit.isdigit() and isinstance(exp.x_bit, str) and exp.x_bit.isdigit():
                print(f"{exp.expression:<15} {exp.ex_value:<10} {exp.relocatable:<15} "
                    f"{int(exp.n_bit):<10} {int(exp.i_bit):<10} {int(exp.x_bit):<10}")
            else:
                print(f"{exp.expression:<15} {exp.ex_value:<10} {exp.relocatable:<15} "
                    f"{exp.n_bit:<10} {exp.i_bit:<10} {exp.x_bit:<10}")
                
    
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    *** FUNCTION: display_literals ***
    *********************************************************************
    *** DESCRIPTION : This function displays all processed literals in a formatted table.
    *** It shows the literal name, its calculated value, length in bytes, and address.
    *** INPUT ARGS : None
    *** OUTPUT ARGS : None
    *** IN/OUT ARGS : None
    *** RETURN : None
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def display_literals(self):
        print()
        print("\t\tLITERAL TABLE")
        print("----------------------------------------------")
        print(f"{'NAME':<15} {'VALUE':<10} {'LENGTH':<10} {'ADDRESS':<10}")
        print("----------------------------------------------")
        for lit in self.literals:
            print(f"{lit.name:<15} {lit.value:<10} {lit.length:<10} {lit.address:<10}")
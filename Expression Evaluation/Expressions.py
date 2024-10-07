from BST import BinarySearchTree
import re

class Expression:
    def __init__(self, expression, ex_value, relocatable, n_bit=False, i_bit=False, x_bit=False):
        self.expression = expression
        self.ex_value = ex_value
        self.relocatable = relocatable
        self.n_bit = n_bit
        self.i_bit = i_bit
        self.x_bit = x_bit


class Literal:
    def __init__(self, name, value, length, address):
        self.name = name
        self.value = value
        self.length = length
        self.address = address


class ExpressionVerifier:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.expressions = []
        self.literals = []
        self.literal_address_counter = 0

    def verify_expression(self, expression):
        n_bit = i_bit = x_bit = False
        relocatable = "ABSOLUTE"
        value = None
        original_expression = expression.strip()

        # Check for special cases like @, #, and ,
        if expression.startswith('@'):
            expression = expression[1:]  # Remove '@'
            n_bit = True  # Set n-bit
        elif expression.startswith('#'):
            expression = expression[1:]  # Remove '#'
            i_bit = True  # Set i-bit
        else:
            # If the symbol is standard (not @ or #), both n_bit and i_bit should be True
            n_bit = i_bit = True
            
        # Handle expressions starting with "=" to add to literal table
        if expression.startswith('='):
            literal_value, length = self.process_literal(expression)
            if literal_value:
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
            op1, op2 = expression.split('+')
            if op1[1:].isdigit():
                op1 = int(op1.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op2)
                value += op1  # Adding the number to the symbol's value
            else:
                op2 = int(op2.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op1)
                value += op2  # Adding the number to the symbol's value

        elif '-' in expression:
            op1, op2 = expression.split('-')
            if op1[1:].isdigit():
                op1 = int(op1.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op2)
                value -= op1  # Adding the number to the symbol's value
            else:
                op2 = int(op2.lstrip('#'))  # Remove the '#' before number
                value, relocatable = self.lookup_symbol(op1)
                value -= op2  # Adding the number to the symbol's value
        else:
            value, relocatable = self.lookup_symbol(expression)

        # Add valid expression to the list
        new_expression = Expression(original_expression, value, relocatable, n_bit, i_bit, x_bit)
        self.expressions.append(new_expression)

    def lookup_symbol(self, symbol):
        # Use the symbol table to look up the symbol in the BST
        node = self.symbol_table.search_symbol(symbol)
        if node:
            return node.value, "RELATIVE" if node.rflag else "ABSOLUTE"
        else:
            raise ValueError(f"Symbol {symbol} not found in the Symbol Table")

    def process_literal(self, literal):
        # Keep the full literal name, including the '='

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
        elif literal.startswith('=0X'):
            hex_part = literal[3:]  # Skip the 'X'
            try:
                literal_value = hex_part  # Convert hexadecimal to decimal
                length = 1
            except ValueError:
                raise ValueError(f"Invalid hexadecimal literal: {literal}")
        else:
            raise ValueError(f"Unsupported literal format: {literal}")

        # Add the new literal to the table with the '=' included in the name
        self.literal_address_counter += 1
        return literal_value, length



    def display_expressions(self):
        print()
        print("\t\t\tEXPRESSIONS")
        print("----------------------------------------------------------------------")
        print(f"{'EXPRESSION':<15} {'VALUE':<10} {'RELOCATABLE':<15} {'N-Bit':<10} {'I-Bit':<10} {'X-Bit':<10}")
        for exp in self.expressions:
            print(f"{exp.expression:<15} {exp.ex_value:<10} {exp.relocatable:<15} "
                  f"{int(exp.n_bit):<10} {int(exp.i_bit):<10} {int(exp.x_bit):<10}")

    def display_literals(self):
        print()
        print("\t\tLITERAL TABLE")
        print("----------------------------------------------")
        print(f"{'NAME':<15} {'VALUE':<10} {'LENGTH':<10} {'ADDRESS':<10}")
        for lit in self.literals:
            print(f"{lit.name:<15} {lit.value:<10} {lit.length:<10} {lit.address:<10}")
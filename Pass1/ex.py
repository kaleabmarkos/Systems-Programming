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
        value = 0
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
                expression = expression[1:]  # Remove '@'
            else:        
                expression = expression[1:]  # Remove '@'
                n_bit = True  # Set n-bit
        
        elif expression.startswith('#'):
            if expression[1:].isdigit():
                # Check if the expression is purely numeric (like 22)
                calc_expression = expression[1:]
                # Treat as an immediate value
                value = int(calc_expression)
                i_bit = True  # Set the immediate addressing bit to true
                # Add the expression to the table (e.g., it would show as "#22")
                new_expression = Expression(f"{expression}", value, relocatable, n_bit, i_bit, x_bit)
                self.expressions.append(new_expression)
                return  # Skip further processing since it's a valid numeric expression
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
            relocatable_of_op1=relocatable_of_op2=None
            
            if op1.isdigit():
                value=int(op1)
                relocatable_of_op1 = "ABSOLUTE"
            elif op1[0].isalpha():
                op1_value, relocatable_of_op1 = self.lookup_symbol(op1)
                
                if not op1_value:
                    new_expression = Expression(f"{original_expression}", '-', '-', '-', '-', f'- \t<- This is not applicable b/c one of the symbols is not in the symbol table')
                    self.expressions.append(new_expression)
                    return
                value += op1_value  # Adding the number to the symbol's value
            elif op1[1:].isdigit():
                op1 = int(op1.lstrip('#'))  # Remove the '#' before number
                relocatable_of_op1 = "ABSOLUTE"
                value = op1  # Adding the number to the symbol's value
            if op2.isdigit():
                value+=int(op2)
                relocatable_of_op2 = "ABSOLUTE"
            elif op2[0].isalpha():
                op2_value, relocatable_of_op2 = self.lookup_symbol(op2)
                if not op2_value:
                    new_expression = Expression(f"{original_expression}", '-', '-', '-', '-', f'- \t<- This is not applicable b/c one of the symbols is not in the symbol table')
                    self.expressions.append(new_expression)
                    return
                value += op2_value  # Adding the number to the symbol's value
            elif op2[1:].isdigit():
                op2 = int(op2.lstrip('#'))  # Remove the '#' before number
                relocatable_of_op2 = "ABSOLUTE"
                value += op2  # Adding the number to the symbol's value
            
            if relocatable_of_op1 and relocatable_of_op2:
            
                # Handle addition relocatability
                if (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "RELATIVE"):
                    relocatable = "RELATIVE"
                elif (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "ABSOLUTE"):
                    relocatable = "ABSOLUTE"
                elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "ABSOLUTE"):
                    relocatable = "RELATIVE"
                elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "RELATIVE"):
                    relocatable = "RR"
    
                

        elif '-' in expression:
            op1, op2 = map(str.strip, expression.split('-'))
            relocatable_of_op1=relocatable_of_op2=None

            if op1.isdigit():
                value=int(op1)
                relocatable_of_op1 = "ABSOLUTE"
            elif op1[0].isalpha():
                op1_value, relocatable_of_op1 = self.lookup_symbol(op1) 
                if not op1_value:
                    new_expression = Expression(f"{original_expression}", '-', '-', '-', '-', f'- \t<- This is not applicable b/c one of the symbols is not in the symbol table')
                    self.expressions.append(new_expression)
                    return
                value =op1_value  # Adding the number to the symbol's value
                
            elif op1[1:].isdigit():
                op1 = int(op1.lstrip('#'))  # Remove the '#' before number
                relocatable_of_op1 = "ABSOLUTE"
                value = op1  # Adding the number to the symbol's value
            if op2.isdigit():
                value=value-int(op2)
                relocatable_of_op2 = "ABSOLUTE"
            elif op2[0].isalpha():
                op2_value, relocatable_of_op2 = self.lookup_symbol(op2)
                if not op2_value:
                    new_expression = Expression(f"{original_expression}", '-', '-', '-', '-', f'- \t<- This is not applicable b/c one of the symbols is not in the symbol table')
                    self.expressions.append(new_expression)
                    return
                value =value - op2_value  # Adding the number to the symbol's value
            elif op2[1:].isdigit():
                op2 = int(op2.lstrip('#'))  # Remove the '#' before number
                relocatable_of_op2 = "ABSOLUTE"
                value =value - op2  # Adding the number to the symbol's value

            if relocatable_of_op1 and relocatable_of_op2:
        
                # Handle subtraction relocatability
                if (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "RELATIVE"):
                    new_expression = Expression(f"{original_expression}->(ER)", '-', '-', '-', '-', '- \t<- Error: ABSOLUTE - RELATIVE is not allowed')
                    self.expressions.append(new_expression)
                    return
                elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "RELATIVE"):
                    relocatable = "ABSOLUTE"
                elif (relocatable_of_op1 == "RELATIVE" and relocatable_of_op2 == "ABSOLUTE"):
                    relocatable = "RELATIVE"
                elif (relocatable_of_op1 == "ABSOLUTE" and relocatable_of_op2 == "ABSOLUTE"):
                    relocatable = "ABSOLUTE"

        
        else:
            value, relocatable = self.lookup_symbol(expression)

        if value and (relocatable != "AR" and relocatable != "RR"):
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
        return self.expressions
        

    
    def lookup_symbol(self, symbol):
        # Use the symbol table to look up the symbol in the BST
        node = self.symbol_table.search_symbol(symbol.strip())
        if node:
            return node.value, "RELATIVE" if node.rflag else "ABSOLUTE"
        else:
            return None, f"Symbol {symbol} not found in the Symbol Table"
        
    

    def process_literal(self, literal):

        # Check if the literal already exists
        for lit in self.literals:
            if lit.name == literal:
                return None,0  # If found, return the existing literal value
        length=0
        # If the first character is 'C', treat the following characters as ASCII
        if literal.startswith('=0C') or literal.startswith('=0c'):
            ascii_part = literal[3:]  # Skip the 'C'
            ascii_value = ''.join(str(hex(ord(char))[2:]) for char in ascii_part)  # Convert each character to its ASCII code
            literal_value = ascii_value
            length = len(literal[3:])
            self.literal_address_counter += 1
            
        elif literal.startswith('=0X') or literal.startswith('=0x'):
            hex_part = literal[3:]  # Skip the 'X'
            literal_value = hex_part  # Take the hexpart
            length = 1
            self.literal_address_counter += 1
        else:
            return '-', 0

        return literal_value, length    

    
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
                
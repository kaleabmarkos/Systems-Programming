from ex import ExpressionVerifier  # Import the ExpressionVerifier class

class EquProcessor:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.expr_verifier = ExpressionVerifier(symbol_table)  # Pass the symbol table to the verifier

    def process_equ(self, operand):
        """Process the operand of the EQU directive."""
        # Use the ExpressionVerifier to calculate the value of the operand
        calculated_value = self.expr_verifier.verify_expression(operand)

        if calculated_value:  # Assuming it returns a valid value
            return calculated_value[-1].ex_value  # Get the last value in the expressions
        else:
            return None  # Or handle an error appropriately

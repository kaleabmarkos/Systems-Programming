from opstore import OpcodeClass
from ex import ExpressionVerifier

class Assembler:
    def __init__(self):
        self.opcode_class = OpcodeClass()
        self.symbol_table = {}
        self.location_counter = 0
        self.output_lines = []
        self.literal = []

    def load_opcodes(self):
        """Load opcodes from the file."""
        self.opcode_class.load_opcodes_from_file()

    def process_assembly_file(self, filename):
        """Process the assembly input file."""
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('.'):  # Ignore comments
                        self.parse_line(line)
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")

    def parse_line(self, line):
        """Parse a line from the assembly file."""
        parts = line.split()
        if not parts:
            return

        # Initialize label
        label = ''

        # Handle label
        if parts[0].endswith(':'):
            label = parts[0] # Remove the colon
            self.symbol_table[label] = self.location_counter
            parts = parts[1:]  # Remove the label from parts

        # Handle opcode and operand
        if parts:
            opcode = parts[0]
            operand = ' '.join(parts[1:]) if len(parts) > 1 else ''
            
            # Process directives
            if opcode == 'START':
                self.location_counter = int(operand, 16)  # Set the location counter
                
            elif opcode == 'END':
                return  # Skip further processing for END

            elif opcode == 'WORD':
                self.location_counter += 3  # WORD takes 3 bytes

            elif opcode == 'BYTE':
                if operand.startswith('='):
                    length = (len(operand) - 3) // 2 if operand.startswith('=0X') or operand.startswith('=0x') else len(operand) - 3
                    self.location_counter += length

            elif opcode == 'RESB':
                self.location_counter += int(operand)  # Add the specified number
                
            elif opcode == 'RESW':
                self.location_counter += int(operand) * 3  # Add 3 times the specified number
                
            elif opcode == 'BASE':
                pass  # No action required

            elif opcode == 'EQU':
                self.handle_equ(operand, label)  # New method for handling EQU

            format_ = self.opcode_class.get_opcode_format(opcode)
            # Append the output line with the current line data
            self.output_lines.append(f"{self.location_counter:05X}\t{label if label else '':<10}\t{opcode}\t{operand}")
            self.location_counter += format_  # Increment LC by the format of the opcode

    def handle_equ(self, operand, label):
        """Handle the EQU directive by calculating the value of the operand."""
        expression_parts = [part.strip() for part in operand.replace('+', ' + ').replace('-', ' - ').split()]

        calculated_value = 0
        error_occurred = False

        for part in expression_parts:
            if part in self.symbol_table:
                calculated_value += self.symbol_table[part]  # Add the value from the symbol table
            elif part.isdigit():  # Check if it's a numeric value
                calculated_value += int(part)
            elif part in ['+', '-']:  # Ignore operations
                continue
            else:
                print(f"Error: Symbol '{part}' not found in the symbol table.")
                error_occurred = True

        if not error_occurred:
            # Store the calculated value in the symbol table
            self.symbol_table[label] = calculated_value  # Set the value of the label to the calculated value
            print(f"Calculated {label} as {calculated_value}.")


    def generate_output_file(self, output_filename):
        """Generate the output file."""
        with open(output_filename, 'w') as file:
            file.write("Sym Table\n")
            for symbol, address in self.symbol_table.items():
                file.write(f"{symbol:<10}{address:05X}  true\n")  # Print symbol and its address with alignment

            file.write(f"\nProgram Length is {self.location_counter:05X} bytes\n\n")
            file.write("Output Listing:\n")
            file.write(f"{'LOCCTR':<10} {'Symbol':<10} {'Opcode':<10} {'Operand'}\n")  # Header
            file.write('-' * 50 + '\n')  # Separator
            for line in self.output_lines:
                locctr, sym, opcode, operand = line.split('\t')
                file.write(f"{locctr:<10} {sym:<10} {opcode:<10} {operand}\n")

# Example Usage
if __name__ == "__main__":
    assembler = Assembler()
    assembler.load_opcodes()
    assembler.process_assembly_file('p0.asm')  # Assuming p0.asm is the input file
    assembler.generate_output_file('p0.int')  # Generate the output file

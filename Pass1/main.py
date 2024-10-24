from opstore import OpcodeClass

class Assembler:
    def __init__(self):
        self.opcode_class = OpcodeClass()
        self.symbol_table = {}
        self.location_counter = 0
        self.output_lines = []

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

        label = ''
        # Handle label
        if parts[0].endswith(':'):
            label = parts[0]  # Remove the colon
            self.symbol_table[label] = self.location_counter
            parts = parts[1:]  # Remove the label from parts

        # Handle opcode
        if parts:
            opcode = parts[0]
            operand = ' '.join(parts[1:]) if len(parts) > 1 else ''
            format = self.opcode_class.get_opcode_contents()
            format_=0
            if opcode.startswith('+'):
                format_ = 4
            else:
                for form in format:
                    if form[0]==opcode:
                        format_ = int(form[1]) 
            self.output_lines.append(f"{self.location_counter:05X}\t{label}\t{opcode}\t{operand}")  # Store the current line
            self.location_counter += format_  # Increment LC by the format of the opcode


    def generate_output_file(self, output_filename):
        """Generate the output file."""
        with open(output_filename, 'w') as file:
            
            counter=1
            file.write(f"\nProgram Length is {self.location_counter:05X} bytes\n\n")
            file.write("Output Listing:\n")
            file.write(f"{'LINE #':<10}{'LOCCTR':<10} {'Symbol':<10} {'Opcode':<10} {'Operand'}\n")  # Header
            file.write("---------------------------------------------------\n")
            for line in self.output_lines:
                # Ensure the formatting matches the desired output, with correct spacing
                locctr, sym, opcode, operand = line.split('\t')
                file.write(f"{counter:<10}{locctr:<10} {sym:<10} {opcode:<10} {operand}\n")
                counter+=1
            file.write("Sym Table\n")
            for symbol, address in self.symbol_table.items():
                file.write(f"{symbol[:-1]:<10}{address:05X}  true\n")  # Print symbol and its address with alignment

if __name__ == "__main__":
    assembler = Assembler()
    assembler.load_opcodes()
    assembler.process_assembly_file('p0.asm')  # Assuming p0.asm is the input file
    assembler.generate_output_file('p0.lst')  # Generate the output file
class OpcodeDetails:
    def __init__(self, label='', format='', opcode=''):
        self.label = label
        self.format = format
        self.opcode = opcode


class OpcodeClass:
    def __init__(self):
        self.opcode_table = []  # List to store opcode details

    def get_opcode_contents(self):
        """Return the list of opcodes."""
        return [(opcode.label, opcode.format) for opcode in self.opcode_table]

    def break_opcode_details(self, line):
        """Parse a line and create an OpcodeDetails object."""
        line = line.strip()  # Remove leading/trailing whitespace
        parts = line.split()  # Split the line into components
        label = ''
        format_ = ''
        opcode = ''

        for i, element in enumerate(parts):
            if element:  # Only process non-empty elements
                if i == 0:
                    label = element
                elif i == 1:
                    opcode = element
                else:
                    format_ = element

        return OpcodeDetails(label, format_, opcode)

    def add_opcode(self, opcode_lines):
        """Process lines and add OpcodeDetails to the table."""
        for line in opcode_lines:
            opcode_obj = self.break_opcode_details(line)
            self.opcode_table.append(opcode_obj)

    def load_opcodes_from_file(self):
        """Load opcode details from a file."""
        filename='./OPCODE.DAT'
        try:
            with open(filename, 'r') as file:
                opcode_lines = file.readlines()
                self.add_opcode(opcode_lines)  # Add opcodes from the file
                
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def print_them(self):
        return [(opcode.label, opcode.format) for opcode in self.opcode_table]

if __name__ == "__main__":
    opcode_class = OpcodeClass()
    
    # Load opcodes from 'opcode.dat' automatically
    opcode_class.load_opcodes_from_file()
    print(opcode_class.print_them())
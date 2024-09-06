#Define a Node class

#Define a BinarySearchTree class
    # a function to insert
    # a function to search
    # a function to traverse (in order)

#File parsing and Error Handling

#Main Function

class Node:
    def __init__(self, symbol, value, rflag):
        self.symbol = symbol[:4].upper()
        self.value = value
        self.rflag = rflag
        self.iflag = True
        self.mflag = False
        self.left = None
        self.right = None
    
    def __repr__(self) -> str:
        return f"{self.symbol}: {self.value} {self.rflag} {self.iflag} {self.mflag}"

class BinarySearchTree:
    def __init__(self):
        self.node = None
    
    def insert(self, symbol, value, rflag):
        if self.node is None:
            new_node = Node(symbol, value, rflag)
        else:
            self.insert_recursivly(self.node, symbol,value, rflag)
    
    def insert_recursivly(self, cur_node ,symbol, value, rflag):
        if symbol[:4].upper() < cur_node.symbol:
            if cur_node.left is None:
                cur_node.left = Node(symbol, value, rflag)
            else:
                self.insert_recursivly(cur_node.left, symbol,value,rflag)
        if symbol[:4].upper() > cur_node.symbol:
            if cur_node.right is None:
                cur_node.right = Node(symbol, value, rflag)
            else:
                self.insert_recursivly(cur_node.right, symbol, value, rflag)
        else:
            cur_node.mflag = True
    
    def search(self, node, symbol):
        self.search_recusive(node,symbol)
    
    def search_recursive(self, curr_node, symbol):
        if curr_node is None:
            return None
        
        if symbol[:4] == curr_node.symbol:
            return f'symbol found'
        
        elif symbol[:4] < curr_node.symbol:
            self.search_recursive(curr_node.left, symbol)
        
        else:
            self.search_recursive(curr_node.right, symbol)
    
    def traversal(self, node):
        self.inorder_traversal(node)
    
    def inorder_traversal(self,curr_node):
        if curr_node:
            self.inorder_traversal(curr_node.left)
            print(f"{curr_node.symbol}: {curr_node.value} {curr_node.rflag} {curr_node.mflag} {curr_node.iflag}")
            self.inorder_traversal(curr_node.right)
    
def Main():
    def process_sys_dat(bst, dat_file):
        try:
            with open(dat_file,'r') as file:
                for line in file:
                    parts = line.split()
                    if len(parts) < 4:
                        print('Invalid line format')
                        continue
                    
                    symbol = parts[0].replace(':','')
                    value = parts[1]
                    rflag = parts[2].lower()

                    if not (symbol[0].isalpa()) or len(symbol) > 10 or not all(i.isalnum() or i == '_' for i in symbol):
                        print(f'ERROR: Invalid symbol: {symbol}')
                        continue

                    try:
                        int(value)
                    except ValueError:
                        print(f'ERROR: Invalid value: {value}')
                        continue
                    
                    if rflag not in ['true','false']:
                        print(f'ERROR: Invalid rflag: {rflag}')
                        continue
                bst.insert(symbol, value, rflag)

        except FileNotFoundError:
            raise    

            
        
    
    def process_search_file():
        ...

    bst = BinarySearchTree()

    try:
        process_sys_dat(bst, 'SYMS.DAT')
    except FileNotFoundError:
        print("ERROR: File not found")
        return
    
    search_file = input("What is the search file name? ")
    process_search_file(search_file)
    

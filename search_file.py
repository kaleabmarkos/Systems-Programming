#Define a Node class

#Define a BinarySearchTree class
    # a function to insert
    # a function to search
    # a function to traverse (in order)


#Main Function
    #File parsing and Error Handling

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
            self.node = Node(symbol, value, rflag)
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
    
    def search(self, symbol):
        self.search_recursive(self.node,symbol)
    
    def search_recursive(self, curr_node, symbol):
        if curr_node is None:
            return None
        
        if symbol[:4] == curr_node.symbol:
            return f'{symbol}'
        
        elif symbol[:4] < curr_node.symbol:
            self.search_recursive(curr_node.left, symbol)
        
        else:
            self.search_recursive(curr_node.right, symbol)
    
    def inorder_traversal(self):
        self.inorder_traversal_func(self.node)
    
    def inorder_traversal_func(self,curr_node):
        if curr_node:
            self.inorder_traversal_func(curr_node.left)
            print(f"{curr_node.symbol}: {curr_node.value} {curr_node.rflag} {curr_node.mflag} {curr_node.iflag}")
            self.inorder_traversal_func(curr_node.right)
    
def main():
    def process_sys_dat(bst, dat_file):
        try:
            with open(dat_file,'r') as file:
                for line in file:
                    parts = line.split()
                    if len(parts) < 3:
                        print('Invalid line format')
                        continue
                    
                    symbol = parts[0].replace(':','')
                    value = parts[1]
                    rflag = parts[2].lower()

                    if not (symbol[0].isalpha()) or len(symbol) > 10 or not all(i.isalnum() or i == '_' for i in symbol):
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


    def process_search_file(bst, search_file):
        try:
            with open(search_file,'r') as file:
                for line in file:
                    symbol = line.strip()
                    node = bst.search(symbol)
                    if node:
                        print(f'Symbol found: {node}')
                    else:
                        print('ERROR: Symbol not found')
        
        except FileNotFoundError:
            raise

    bst = BinarySearchTree()

    try:
        process_sys_dat(bst, 'SYMS.DAT')
    except FileNotFoundError:
        print("ERROR: SYMS.DAT not found")
        return
    
    search_file = input("What is the search file name? ")
    
    try:
        process_search_file(bst, search_file)
    except FileNotFoundError:
        print(f"ERROR: {search_file} not found")
        return

    print('Symbole Table in an in-order traversal')
    bst.inorder_traversal()

    
if __name__ == "__main__":
    main()
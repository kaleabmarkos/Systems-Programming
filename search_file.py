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
    
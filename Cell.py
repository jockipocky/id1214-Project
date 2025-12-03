
class Cell:

    def __init__(self,row,column,value = None): # self specific instance being created
        self.row = row
        self.column = column
        self.value = value
        self.candidates = set()
        
    def __repr__(self):
            return f"Cell(r={self.row}, c={self.column}, v={self.value}, cand={self.candidates})"
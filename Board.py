from Cell import Cell

class Board:
    def __init__(self, initial_grid):
        """
        initial_grid: 9x9 list of ints from UI (0 = empty, 1–9 = given value)
        """
        self.size = len(initial_grid)
        self.cells = []          # 2D list of Cell objects
        self.givens = set()      # coordinates (row, col) that were given from the start

        for r in range(self.size):
            row = []
            for c in range(self.size):
                value = initial_grid[r][c]
                if value == 0:
                    cell = Cell(r, c, None)   # None = empty
                else:
                    cell = Cell(r, c, value)
                    self.givens.add((r, c))
                row.append(cell)
            self.cells.append(row)

    def get_value(self, row, col):
        return self.cells[row][col].value

    def set_value(self, row, col, value):
        self.cells[row][col].value = value

    def is_given(self, row, col):
        """Return True if this cell was part of the original puzzle."""
        return (row, col) in self.givens

    def to_grid(self):
        """
        Convert back to a 9x9 list of ints (0 for empty) so the UI can display it.
        """
        grid = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                v = self.cells[r][c].value
                row.append(0 if v is None else v)
            grid.append(row)
        return grid
    def print_board(self):
        for r in range(self.size):
            row_values = []
            for c in range(self.size):
                v = self.cells[r][c].value
                row_values.append("." if v is None else str(v))
                if c % 3 == 2 and c != self.size - 1:
                    row_values.append("|")
            print(" ".join(row_values))
            if r % 3 == 2 and r != self.size - 1:
                print("-" * 21)

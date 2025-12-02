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


DIGITS = set(range(1, 10))  # {1,2,3,4,5,6,7,8,9}

def get_row_values(board, row):
    """Return a set of digits already used in a given row."""
    values = set()
    for c in range(board.size):
        v = board.get_value(row, c)
        if v is not None and v != 0:
            values.add(v)
    return values


def get_col_values(board, col):
    """Return a set of digits already used in a given column."""
    values = set()
    for r in range(board.size):
        v = board.get_value(r, col)
        if v is not None and v != 0:
            values.add(v)
    return values


def get_box_values(board, row, col):
    """Return a set of digits already used in the 3x3 box of (row, col)."""
    values = set()

    # Top-left corner of the 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3

    for r in range(box_row_start, box_row_start + 3):
        for c in range(box_col_start, box_col_start + 3):
            v = board.get_value(r, c)
            if v is not None and v != 0:
                values.add(v)
    return values
def get_candidates(board, row, col):
    """
    Return a list of digits that can legally go in (row, col)
    according to Sudoku rules.
    """
    current_value = board.get_value(row, col)
    if current_value is not None and current_value != 0:
        # Cell already filled
        return []

    used = set()
    used |= get_row_values(board, row)
    used |= get_col_values(board, col)
    used |= get_box_values(board, row, col)

    candidates = []
    for d in DIGITS:
        if d not in used:
            candidates.append(d)

    return candidates
def apply_single_candidate_rule(board):
    """
    Go through the whole board.
    If a cell has exactly one candidate, fill it with that value.
    Return True if at least one cell was changed, otherwise False.
    """
    changed = False

    for r in range(board.size):
        for c in range(board.size):
            if board.get_value(r, c) not in (None, 0):
                continue  # already filled

            candidates = get_candidates(board, r, c)
            if len(candidates) == 1:
                board.set_value(r, c, candidates[0])
                changed = True

    return changed

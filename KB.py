from Board import Board
from Cell import Cell

class KnowledgeBase:
    def __init__(self, board):
        self.board = board
        self.rules = []  # list of rule functions
        self.initialize_candidates()

    def add_rule(self, rule_func):
        self.rules.append(rule_func)

    def initialize_candidates(self):
        """
        For every cell:
        - if it's empty, compute candidates and store them in cell.candidates
        - if it's filled, candidates is an empty set
        """
        for r in range(self.board.size):
            for c in range(self.board.size):
                cell = self.board.cells[r][c]
                if cell.value in (None, 0):
                    cell.candidates = set(get_candidates(self.board, r, c))
                else:
                    cell.candidates = set()

DIGITS = set(range(1, 10))  # {1,2,3,4,5,6,7,8,9}

# Constraint
def get_row_values(board, row):
    """Return a set of digits already used in a given row."""
    values = set()
    for c in range(board.size):
        v = board.get_value(row, c)
        if v is not None and v != 0:
            values.add(v)
    return values

# Constraint
def get_col_values(board, col):
    """Return a set of digits already used in a given column."""
    values = set()
    for r in range(board.size):
        v = board.get_value(r, col)
        if v is not None and v != 0:
            values.add(v)
    return values

# Constraint
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

# Constraint application
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

# Rule
def apply_single_candidate_rule(board):
    """
    If a cell has exactly one candidate in its stored candidate set,
    fill it and clear its candidates, then propagate constraints.
    """
    changed = False

    for r in range(board.size):
        for c in range(board.size):
            cell = board.cells[r][c]

            # Skip filled cells
            if cell.value not in (None, 0):
                continue

            # Make sure candidates available
            if not cell.candidates:
                cell.candidates = set(get_candidates(board, r, c))

            # ------ Single candidate detected ------
            if len(cell.candidates) == 1:
                value = next(iter(cell.candidates))

                # Set cell value
                cell.value = value
                cell.candidates.clear()
                changed = True

                # NEW: Propagate value to remove it from other cells' candidates
                propagate_value(board, r, c, value)

    return changed


def apply_hidden_single_rule(board):
    """ 
    Hidden Single: if a digit can only go in one cell in a group (row, col, box), fill it.
    """
    changed = False

    def check_group(cells):
        """
        cells: list of (row, col) positions in the group
        """
        nonlocal changed
        for d in DIGITS:
            positions = []
            for r, c in cells:
                if board.get_value(r, c) in (None, 0):
                    if d in get_candidates(board, r, c):
                        positions.append((r, c))
            if len(positions) == 1:
                row, col = positions[0]
                cell = board.cells[row][col]
                cell.value = d
                cell.candidates.clear()
                propagate_value(board, row, col, d)
                changed = True

    size = board.size

    # --- Rows ---
    for r in range(size):
        cells = [(r, c) for c in range(size)]
        check_group(cells)

    # --- Columns ---
    for c in range(size):
        cells = [(r, c) for r in range(size)]
        check_group(cells)

    # --- Boxes ---
    for box_row in range(0, size, 3):
        for box_col in range(0, size, 3):
            cells = [
                (r, c)
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
            ]
            check_group(cells)

    return changed

def is_row_valid(board, row):
    values = [
        board.get_value(row, c)
        for c in range(board.size)
        if board.get_value(row, c) not in (None, 0)
    ]
    return len(values) == len(set(values))

def is_col_valid(board, col):
    values = [
        board.get_value(r, col)
        for r in range(board.size)
        if board.get_value(r, col) not in (None, 0)
    ]
    return len(values) == len(set(values))

def is_box_valid(board, row, col):
    values = []
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for r in range(box_row_start, box_row_start + 3):
        for c in range(box_col_start, box_col_start + 3):
            v = board.get_value(r, c)
            if v not in (None, 0):
                values.append(v)
    return len(values) == len(set(values))

def is_board_valid(board):
    size = board.size
    for r in range(size):
        if not is_row_valid(board, r):
            return False
    for c in range(size):
        if not is_col_valid(board, c):
            return False
    for r in range(0, size, 3):
        for c in range(0, size, 3):
            if not is_box_valid(board, r, c):
                return False
    return True

def is_solved(board):
    for r in range(board.size):
        for c in range(board.size):
            if board.get_value(r, c) in (None, 0):
                return False
            
    return is_board_valid(board)

def propagate_value(board, row, col, value):
    """
    When (row, col) is set to `value`, remove that value
    from the candidate sets of all other cells in the same
    row, column, and 3×3 box.
    """
    size = board.size

    # --- Remove from row ---
    for c in range(size):
        if c != col:
            cell = board.cells[row][c]
            if value in cell.candidates:
                cell.candidates.discard(value)

    # --- Remove from column ---
    for r in range(size):
        if r != row:
            cell = board.cells[r][col]
            if value in cell.candidates:
                cell.candidates.discard(value)

    # --- Remove from box ---
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3

    for r in range(box_row_start, box_row_start + 3):
        for c in range(box_col_start, box_col_start + 3):
            if r == row and c == col:
                continue
            cell = board.cells[r][c]
            if value in cell.candidates:
                cell.candidates.discard(value)



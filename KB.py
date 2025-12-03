class KnowledgeBase:
    def __init__(self, board):
        self.board = board
        self.rules = []  # list of rule functions

    def add_rule(self, rule_func):
        self.rules.append(rule_func)

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
def apply_single_candidate_rule(board, logs=None):
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

            if logs is not None:
                logs.append(f"Single Candidate filled {candidates[0]} at ({r}, {c})")

    return changed

def apply_hidden_single_rule(board, logs=None):
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
                board.set_value(row, col, d)
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

     

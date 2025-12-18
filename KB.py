from Board import Board
from Cell import Cell
import copy

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

# ----------------------------
# Constraint helpers
# ----------------------------

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

# ----------------------------
# Rules
# ----------------------------

def apply_single_candidate_rule(board, logger=None):
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
            if not hasattr(cell, "candidates") or not cell.candidates:
                cell.candidates = set(get_candidates(board, r, c))

            if len(cell.candidates) == 1:
                value = next(iter(cell.candidates))
                old_value = cell.value
                old_candidates = set(cell.candidates)

                cell.value = value
                cell.candidates.clear()
                propagate_value(board, r, c, value)
                changed = True

                if logger is not None:
                    logger.add_rule_change(
                        rule_name="single_candidate",
                        row=r,
                        col=c,
                        old_value=old_value,
                        new_value=value,
                        reason="Cell had exactly one candidate",
                        extra={"candidates_before": list(old_candidates)},
                    )

    return changed


def apply_hidden_single_rule(board, logger=None):
    """Hidden Single: if a digit can only go in one cell in a group, fill it."""
    changed = False

    def check_group(cells):
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
                old_value = cell.value

                cell.value = d
                cell.candidates = set()  # no candidates left
                propagate_value(board, row, col, d)
                changed = True

                if logger is not None:
                    logger.add_rule_change(
                        rule_name="hidden_single",
                        row=row,
                        col=col,
                        old_value=old_value,
                        new_value=d,
                        reason="Digit can only go in one cell in this group",
                    )

    size = board.size

    # Rows
    for r in range(size):
        cells = [(r, c) for c in range(size)]
        check_group(cells)

    # Columns
    for c in range(size):
        cells = [(r, c) for r in range(size)]
        check_group(cells)

    # Boxes
    for box_row in range(0, size, 3):
        for box_col in range(0, size, 3):
            cells = [
                (r, c)
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
            ]
            check_group(cells)

    return changed

# ----------------------------
# Board validity helpers
# ----------------------------

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

# ----------------------------
# Candidate propagation
# ----------------------------

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
            if hasattr(cell, "candidates") and value in cell.candidates:
                cell.candidates.discard(value)

    # --- Remove from column ---
    for r in range(size):
        if r != row:
            cell = board.cells[r][col]
            if hasattr(cell, "candidates") and value in cell.candidates:
                cell.candidates.discard(value)

    # --- Remove from box ---
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3

    for r in range(box_row_start, box_row_start + 3):
        for c in range(box_col_start, box_col_start + 3):
            if r == row and c == col:
                continue
            cell = board.cells[r][c]
            if hasattr(cell, "candidates") and value in cell.candidates:
                cell.candidates.discard(value)

# ----------------------------
# Utility for search
# ----------------------------

def find_empty_cell(board):
    """Return (row, col) of the first empty cell, or None if full."""
    for r in range(board.size):
        for c in range(board.size):
            if board.get_value(r, c) in (None, 0):
                return (r, c)
    return None

def apply_rules_until_stable(board, logger=None):
    """
    Apply all simple rules (single candidate, hidden single) repeatedly
    until no more changes occur.
    This is used both by the inference engine and by backtracking branches.
    """
    while True:
        changed = False
        # You can extend this list with more rules later:
        for rule in (apply_single_candidate_rule, apply_hidden_single_rule, apply_naked_triples_rule, apply_naked_pairs_rule):
            if rule(board, logger=logger):
                changed = True
        if not changed:
            break


from itertools import combinations

def _ensure_candidates(board, r, c):
    """Make sure cell.candidates exists and is up-to-date for an empty cell."""
    cell = board.cells[r][c]
    if cell.value not in (None, 0):
        cell.candidates = set()
        return
    if not hasattr(cell, "candidates") or cell.candidates is None or len(cell.candidates) == 0:
        cell.candidates = set(get_candidates(board, r, c))


def _all_units(board):
    """Yield all 27 Sudoku units: 9 rows, 9 cols, 9 boxes. Each unit is a list of (r,c)."""
    size = board.size

    # rows
    for r in range(size):
        yield [(r, c) for c in range(size)]

    # cols
    for c in range(size):
        yield [(r, c) for r in range(size)]

    # boxes
    for br in range(0, size, 3):
        for bc in range(0, size, 3):
            yield [(r, c) for r in range(br, br + 3) for c in range(bc, bc + 3)]


def apply_naked_pairs_rule(board, logger=None):
    """
    Naked Pairs:
    If two cells in a unit have the exact same two candidates {a,b},
    remove {a,b} from all other cells in that unit.
    """
    changed = False

    for unit in _all_units(board):
        # ensure candidates for empty cells
        empties = []
        for (r, c) in unit:
            if board.get_value(r, c) in (None, 0):
                _ensure_candidates(board, r, c)
                cell = board.cells[r][c]
                if len(cell.candidates) == 2:
                    empties.append((r, c, frozenset(cell.candidates)))

        # group by candidate-pair
        pair_map = {}
        for r, c, candset in empties:
            pair_map.setdefault(candset, []).append((r, c))

        # if a pair appears in exactly 2 cells -> eliminate from others
        for pair_cands, cells_with_pair in pair_map.items():
            if len(cells_with_pair) != 2:
                continue

            for (r, c) in unit:
                if (r, c) in cells_with_pair:
                    continue
                if board.get_value(r, c) not in (None, 0):
                    continue

                _ensure_candidates(board, r, c)
                cell = board.cells[r][c]

                before = set(cell.candidates)
                to_remove = set(pair_cands) & before
                if to_remove:
                    cell.candidates -= to_remove
                    changed = True
                    if logger is not None:
                        logger.add_elimination(
                            rule_name="naked_pairs",
                            row=r,
                            col=c,
                            removed=to_remove,
                            reason=f"because cells {cells_with_pair} form a naked pair {sorted(pair_cands)}"
                        )



    return changed


def apply_naked_triples_rule(board, logger=None):
    """
    Naked Triples:
    If three cells in a unit have candidates whose UNION is exactly 3 digits,
    and each of those three cells' candidates are subsets of that union,
    remove those 3 digits from all other cells in that unit.
    """
    changed = False

    for unit in _all_units(board):
        # collect empty cells with 2 or 3 candidates (typical for triples)
        candidates_list = []
        for (r, c) in unit:
            if board.get_value(r, c) in (None, 0):
                _ensure_candidates(board, r, c)
                cell = board.cells[r][c]
                if 2 <= len(cell.candidates) <= 3:
                    candidates_list.append((r, c, frozenset(cell.candidates)))

        # try all combinations of 3 cells
        for triple in combinations(candidates_list, 3):
            cells = [(triple[0][0], triple[0][1]),
                     (triple[1][0], triple[1][1]),
                     (triple[2][0], triple[2][1])]

            union = set(triple[0][2]) | set(triple[1][2]) | set(triple[2][2])

            # naked triple condition: union size exactly 3
            if len(union) != 3:
                continue

            # each cell candidates must be subset of union
            if not (set(triple[0][2]) <= union and set(triple[1][2]) <= union and set(triple[2][2]) <= union):
                continue

            # eliminate union digits from other cells in unit
            for (r, c) in unit:
                if (r, c) in cells:
                    continue
                if board.get_value(r, c) not in (None, 0):
                    continue

                _ensure_candidates(board, r, c)
                cell = board.cells[r][c]

                before = set(cell.candidates)
                to_remove = union & before
                if to_remove:
                    cell.candidates -= to_remove
                    changed = True
                    if logger is not None:
                        logger.add_elimination(
                            rule_name="naked_triples",
                            row=r,
                            col=c,
                            removed=to_remove,
                            reason=f"because cells {cells} form a naked triple {sorted(union)}"
                        )



    return changed

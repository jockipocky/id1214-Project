from logs import Logger

# IE.py
from KB import (
    KnowledgeBase,
    apply_single_candidate_rule,
    apply_hidden_single_rule,
    is_solved,
    is_board_valid,
    find_empty_cell,
    get_candidates,
)
import copy

class InferenceEngine:
    def __init__(self, board, kb, logger=None):
        """
        board: Board instance
        kb: KnowledgeBase instance
        logger: Logger instance (or None)
        """
        self.board = board
        self.kb = kb
        self.logger = logger

    # -------------------------------------------------
    # 1) RULE-ONLY INFERENCE (no guessing)
    # -------------------------------------------------
    def run_rules_only(self, max_iterations=50):
        """
        Apply all rules in kb.rules repeatedly until no more
        changes or max_iterations is reached.
        This is your "pure inference engine" (no backtracking).
        """
        changed = True
        iteration = 0

        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            if self.logger is not None:
                self.logger.add_iteration(iteration)

            for rule in self.kb.rules:
                result = rule(self.board, logger=self.logger)
                if self.logger is not None:
                    self.logger.add_message(
                        f"Rule {rule.__name__} changed board: {result}"
                    )
                if result:
                    changed = True

        return self.board

    # -------------------------------------------------
    # 2) HYBRID SOLVER: RULES + BACKTRACKING
    # -------------------------------------------------
    def solve(self):
        """
        High-level solve method:
        1) Run rule-based inference first.
        2) If the puzzle is solved, stop.
        3) Otherwise, start backtracking that also uses rules
           in each branch.
        """
        # Phase 1: rules only
        self.run_rules_only()

        if is_solved(self.board):
            return True

        # Phase 2: backtracking + rules
        return self._solve_with_backtracking(self.board, depth=0)

    def _apply_rules_until_stable(self, board):
        """
        Apply core rules repeatedly on a given board until no more changes.
        Uses the same rules as in KnowledgeBase.rules.
        This is used inside backtracking on branch copies.
        """
        while True:
            changed = False
            for rule in (apply_single_candidate_rule, apply_hidden_single_rule):
                if rule(board, logger=self.logger):
                    changed = True
            if not changed:
                break

    def _solve_with_backtracking(self, board, depth=0):
        """
        Backtracking that:
        - Applies rules on each branch (constraint propagation)
        - Uses a deep copy for each guess branch
        - Copies the solution back to self.board when found
        """
        # First, saturate this board with rules
        self._apply_rules_until_stable(board)

        # If solved after rules -> success
        if is_solved(board):
            return True

        # Choose an empty cell to branch on
        empty = find_empty_cell(board)
        if empty is None:
            # Board full but not solved -> invalid
            return is_board_valid(board)

        row, col = empty
        candidates = get_candidates(board, row, col)
        if not candidates:
            return False  # dead end

        for value in candidates:
            old_value = board.get_value(row, col)

            if self.logger is not None:
                self.logger.add_guess(
                    row=row,
                    col=col,
                    old_value=old_value,
                    new_value=value,
                    depth=depth,
                    candidates=candidates,
                    reason="Backtracking guess after inference stalled",
                )

            # Work on a deep copy for this branch
            new_board = copy.deepcopy(board)
            new_board.set_value(row, col, value)

            # Apply rules again after the guess
            self._apply_rules_until_stable(new_board)

            if is_board_valid(new_board):
                # Recurse deeper
                if self._solve_with_backtracking(new_board, depth=depth + 1):
                    # Copy solution from new_board back into the
                    # main engine board (self.board)
                    for r in range(self.board.size):
                        for c in range(self.board.size):
                            self.board.set_value(r, c, new_board.get_value(r, c))
                    return True

            if self.logger is not None:
                self.logger.add_undo(
                    row=row,
                    col=col,
                    old_value=value,
                    new_value=old_value,
                    depth=depth,
                    reason="Guess led to dead end – backtracking",
                )

        return False


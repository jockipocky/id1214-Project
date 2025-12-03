from Board import Board
from KB import (
    KnowledgeBase,
    apply_single_candidate_rule,
    apply_hidden_single_rule,
    is_solved,
)

def run_inference(kb, max_iterations=100):
    """
    Simple inference loop:
    repeatedly apply all rules in kb.rules until
    nothing changes or max_iterations is reached.
    """
    for i in range(max_iterations):
        changed = False
        for rule in kb.rules:
            if rule(kb.board):
                changed = True
        if not changed:
            print(f"No more changes after iteration {i}")
            break

def make_easy_puzzle():
    """
    Very easy puzzle that can be solved by naked + hidden singles.
    0 = empty.
    """
    return [
        [1, 4, 2,  7, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 5, 0,  4, 0, 0],
        [0, 0, 3,  8, 0, 1,  0, 6, 0],

        [6, 9, 0,  0, 0, 0,  0, 0, 0],
        [0, 8, 0,  3, 0, 7,  0, 1, 0],
        [0, 0, 0,  0, 0, 0,  0, 8, 7],

        [0, 3, 0,  6, 0, 8,  5, 0, 0],
        [0, 0, 0,  0, 1, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 9,  3, 7, 1],
    ]

def main():
    grid = make_easy_puzzle()
    board = Board(grid)

    print("Initial board:")
    board.print_board()

    # Set up KB + rules
    kb = KnowledgeBase(board)
    kb.add_rule(apply_single_candidate_rule)
    kb.add_rule(apply_hidden_single_rule)

    # Run inference
    run_inference(kb)

    print("\nAfter inference:")
    board.print_board()

    print("\nSolved?", is_solved(board))

if __name__ == "__main__":
    main()

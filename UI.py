from Board import Board
from KB import KnowledgeBase, apply_single_candidate_rule, apply_hidden_single_rule, apply_naked_triples_rule, apply_naked_pairs_rule
from IE import InferenceEngine
from logs import Logger

def parse_puzzle(puzzle_str):
    """
    Convert a string of 81 digits (0 = empty) into a 9x9 grid.
    Example: "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    """
    if len(puzzle_str) != 81 or not puzzle_str.isdigit():
        raise ValueError("Puzzle string must be 81 digits long (0 = empty).")

    grid = []
    for i in range(9):
        row = [int(ch) for ch in puzzle_str[i*9:(i+1)*9]] # slice each row from index 0-9 and converts row to int
        grid.append(row) # add each row to grid
    return grid

def display_grid(grid):
    """Prints a Sudoku grid """
    for r, row in enumerate(grid): # r assigned index and row assinged values at index
        row_str = ""
        for c, num in enumerate(row):
            char = str(num) if num != 0 else "." 
            row_str += char + " "
            if (c + 1) % 3 == 0 and c < 8: # Every third column add vertical seperator for visual 3x3 boxes
                row_str += "| "
        print(row_str)
        if (r + 1) % 3 == 0 and r < 8: # Every third row horizontal sperator for visual 3x3 boxes
            print("- " * 11)



def main():
    #puzzle_str = "000700800006000031040002000024070000010030080000060290000800070860000500002006000"

    puzzles = []
    with open("testpuzzles.txt", "r") as f:
        current_label = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                current_label = line[1:].strip()
            else:
                puzzles.append((current_label, line))

    for label, puzzle_str in puzzles:

        grid = parse_puzzle(puzzle_str)
        board = Board(grid)

        logger = Logger()
        kb = KnowledgeBase(board)

        kb.add_rule(apply_single_candidate_rule)
        kb.add_rule(apply_hidden_single_rule)
        kb.add_rule(apply_naked_pairs_rule)
        kb.add_rule(apply_naked_triples_rule)

        ie = InferenceEngine(board, kb, logger)

        print("Sudoku Puzzle to be solved:")
        print("Difficulty: ", label)
        display_grid(grid)

        # Previously:
        # ie.run()
        # if not is_solved(board):
        #     solve_with_backtracking(board, logger=logger)

        # Now:
        solved = ie.solve()

        print("\nFinal board:")
        board.print_board()
        print("\nSolved?", solved)

        print("\n--- LOG ENTRIES ---")
        logger.print_logs()

if __name__ == "__main__":
    main()
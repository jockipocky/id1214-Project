from Board import Board

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
    # Example puzzle string (0 = empty)
    puzzle_str = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

    # Convert to 2D grid
    grid = parse_puzzle(puzzle_str)

    board = Board(grid) # Create board object based on puzzle_str

    # Display the puzzle
    print("Sudoku Puzzle:")
    display_grid(grid)
    #board.print_board()

if __name__ == "__main__":
    main()

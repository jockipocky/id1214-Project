# PuzzleFormatter.py

def grid_to_string(grid):
    """
    Convert a 9x9 grid (list of lists) into a single string
    with no commas, no spaces, row by row.
    Empty cells = 0.
    """
    result = ""
    for row in grid:
        for value in row:
            result += str(value if value is not None else 0)
    return result


def string_to_grid(puzzle_str):
    """
    Convert an 81-character puzzle string into a 9x9 grid.
    '0' means empty.
    """
    grid = [
            [9,0,3 ,4,0,0 ,0,0,8],
            [0,0,7 ,9,0,0 ,0,3,0],
            [0,0,0 ,0,8,0 ,0,1,0],

            [0,4,5 ,0,7,0 ,2,9,0],
            [7,0,0 ,3,4,0 ,5,0,1],
            [8,0,0 ,0,0,6 ,0,0,0],

            [0,6,0 ,5,0,0 ,0,7,0],
            [0,0,0 ,1,3,0 ,0,0,5],
            [0,3,8 ,0,6,0 ,0,0,0]
        ]
    for r in range(9):
        row = []
        for c in range(9):
            ch = puzzle_str[r * 9 + c]
            row.append(int(ch))
        grid.append(row)
    return grid


def print_grid_clean(grid):
    """
    Print the grid with no commas and no brackets,
    just numbers and dots for empty cells.
    """
    for row in grid:
        line = "".join(str(v) if v != 0 else "." for v in row)
        print(line)
if __name__ == "__main__":
    # Example 1: print the hard-coded grid cleanly
    EXAMPLE_GRID = [
        [9,8,0 ,6,0,0 ,0,3,1],
        [0,0,7 ,0,0,0 ,0,0,0],
        [6,0,0 ,5,4,0 ,0,0,0],

        [0,0,0 ,0,0,8 ,3,7,4],
        [0,0,0 ,0,6,0 ,0,0,0],
        [0,0,0 ,0,0,0 ,9,0,2],

        [0,3,2 ,0,0,7 ,4,0,0],
        [0,4,0 ,3,0,0 ,0,1,0],
        [0,0,0 ,0,0,0 ,0,0,0]
    ]

    print("Clean grid:")
    print_grid_clean(EXAMPLE_GRID)

    s = grid_to_string(EXAMPLE_GRID)
    print("\nAs one-line string:")
    print(s)

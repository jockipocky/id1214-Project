# PuzzleFormatter.py

def grid_to_string(grid):
    """
    Convert a 9x9 grid into a single 81-character string.
    0 or None = empty.
    """
    return "".join(
        str(cell if cell not in (None,) else 0)
        for row in grid
        for cell in row
    )


# ----------------------------
# Manual use
# ----------------------------
if __name__ == "__main__":
    GRID = [
        [0,1,0 ,0,0,0 ,0,0,5],
        [2,6,0 ,4,3,7 ,0,0,0],
        [0,0,4 ,0,0,0 ,0,0,6],

        [0,0,0 ,0,5,0 ,7,0,9],
        [0,0,0 ,7,4,3 ,0,0,2],
        [0,4,0 ,0,0,1 ,0,5,0],

        [0,0,0 ,0,0,6 ,0,9,3],
        [9,0,0 ,0,0,0 ,8,0,7],
        [6,3,0 ,1,7,9 ,0,0,0],
    ]

    print(grid_to_string(GRID))

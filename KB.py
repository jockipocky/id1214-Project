#values for world
SIZE = 9
DIGITS = tuple(range(1,10))
ROWS = tuple(range(SIZE))
COLS = tuple(range(SIZE))

def box_index(row, col):
    return (row // 3) * 3 + (col // 3) # "//" division and removes the decimal, eg 2.6 = 2


ROW_CELLS = {}  # Makes dic for the rows

for r in ROWS:             # For each row number (0 to 8)
    cells_in_row = []      # Start a list for this row

    for c in COLS:         # For each column number (0 to 8)
        cells_in_row.append((r, c))   # Add cell (row, col)

    ROW_CELLS[r] = cells_in_row       # Store full row in the dictionary

COL_CELLS = {}  # Makes dic for col

for c in COLS:              # For each column (0 to 8)
    cells_in_col = []       # One list for this column

    for r in ROWS:          # Check all rows
        cells_in_col.append((r, c))    # Add cell (row, col)

    COL_CELLS[c] = cells_in_col        # Store list in dictionary

BOX_CELLS = {}  # dic for all cells in a box 

for b in range(SIZE):           # Boxes numbered 0–8
    cells_in_box = []           # Start list for this box

    for r in ROWS:              # Check all rows
        for c in COLS:          # Check all columns
            if box_index(r, c) == b:  # Does this cell belong in box b?
                cells_in_box.append((r, c))  # Yes -> store it

    BOX_CELLS[b] = cells_in_box           # Save finished list


#print out the grid
for r in ROWS:
    row_cells = [(r, c) for c in COLS]  # list of coordinates in row r
    print(row_cells)

for box_number, cells in BOX_CELLS.items():
    print(f"Box {box_number}: {cells}")

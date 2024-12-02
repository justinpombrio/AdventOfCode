import sys

DIRECTIONS = {
    "R": (0, +1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (+1, 0)
}

TURNS = {
    "R": "UD",
    "L": "UD",
    "U": "LR",
    "D": "LR"
}

def is_valid(grid, row, col):
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])

grid = []
for line in open(sys.argv[1], 'r'):
    grid.append([int(ch) for ch in line.strip()])

start = [
    (0, 0, 0, "R", 1),
    (0, 0, 0, "D", 1),
]

def next(loc):
    (heat, row, col, direction, spree) = loc
    new_directions = [turn for turn in TURNS[direction]]
    if spree != 3:
        new_directions.append(direction)
    for new_direction in new_directions:
        (delta_row, delta_col) = DIRECTIONS[new_direction]
        (new_row, new_col) = (row + delta_row, col + delta_col)
        if is_valid(grid, new_row, new_col):
            new_spree = spree + 1 if new_direction == direction else 1
            new_heat = heat + grid[new_row][new_col]
            yield (new_heat, new_row, new_col, new_direction, new_spree)

def dominates(loc1, loc2):
    (heat1, row1, col1, dir1, spree1) = loc1
    (heat2, row2, col2, dir2, spree2) = loc2
    return heat1 <= heat2 and row1 == row2 and col1 == col2 and dir1 == dir2 and spree1 <= spree1

def dfs(grid, locs):
    traversed = set()
    while True:
        min_heat = min(map(lambda loc: loc[0], locs))
        for i in range(len(locs)):
            if locs[i][0] == min_heat:
                loc = locs.pop(i)
                break
        for new_loc in next(loc):
            (heat, row, col, d, s) = new_loc
            if row == len(grid) - 1 and col == len(grid[0]) - 1:
                print("Found!", heat)
                sys.exit(1)
            if new_loc not in traversed:
                if not any(map(lambda l: dominates(l, new_loc), locs)):
                    locs.append(new_loc)
                    traversed.add(new_loc)
                    print(new_loc, len(traversed), len(locs))

dfs(grid, start)

import sys
import heapq

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
    (0, 0, 0, "R", 0),
    (0, 0, 0, "D", 0),
]

def next(loc):
    (heat, row, col, direction, spree) = loc
    if spree < 4:
        new_directions = [direction]
    elif spree == 10:
        new_directions = [turn for turn in TURNS[direction]]
    else:
        new_directions = [direction] + [turn for turn in TURNS[direction]]
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
    return heat1 <= heat2 and dir1 == dir2 and spree1 == spree2

def bfs(grid, locs):
    traversed = [[set() for cell in row] for row in grid]
    heapq.heapify(locs)
    while True:
        loc = heapq.heappop(locs)
        if loc[1] == len(grid) - 1 and loc[2] == len(grid[0]) - 1 and loc[4] >= 4:
            print("Found!", loc)
            sys.exit(1)
        for new_loc in next(loc):
            (heat, row, col, d, s) = new_loc
            if new_loc not in traversed[row][col]:
                if not any(map(lambda l: dominates(l, new_loc), traversed[row][col])):
                    heapq.heappush(locs, new_loc)
                    traversed[row][col].add(new_loc)
                    print(new_loc, len(locs))

bfs(grid, start)

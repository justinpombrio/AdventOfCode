import sys

DIRECTIONS = "NESW"

MOVEMENT = {
    # direction -> delta (row, col)
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1)
}

PIPE_SHAPES = {
    # connections for (N, E, S, W)
    ".": (None, None, None, None),
    "|": ("N", None, "S", None),
    "-": (None, "E", None, "W"),
    "L": (None, None, "E", "N"),
    "J": (None, "N", "W", None),
    "7": ("W", "S", None, None),
    "F": ("E", None, None, "S"),
    ".": (None, None, None, None)
}

def is_valid(grid, row, col):
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])

def move_in_dir(grid, row, col, direction):
    (delta_row, delta_col) = MOVEMENT[direction]
    new_row = row + delta_row
    new_col = col + delta_col
    if is_valid(grid, new_row, new_col):
        return (new_row, new_col)
    else:
        return None

def follow_pipe_once(pipe, entry_dir):
    if pipe == "S":
        return "Done"
    else:
        exit_dir = PIPE_SHAPES[pipe][DIRECTIONS.index(entry_dir)]
        if exit_dir is None:
            return None
        return exit_dir

def follow_pipe(grid, row, col, entry_dir):
    direction = entry_dir
    path = [entry_dir]
    while direction in DIRECTIONS:
        new_loc = move_in_dir(grid, row, col, direction)
        print("  ", new_loc)
        if new_loc is None:
            return None
        (row, col) = new_loc
        pipe = grid[row][col]
        exit_dir = follow_pipe_once(pipe, direction)
        print("  ", direction, pipe, exit_dir)
        if exit_dir == "Done":
            return path
        elif exit_dir is None:
            return None
        direction = exit_dir
        path.append(direction)

def area_of_path(path):
    area = 0
    east_west = 0
    for direction in path:
        if direction == "E":
            east_west += 1
        elif direction == "W":
            east_west -= 1
        elif direction == "N":
            area += east_west
        elif direction == "S":
            area -= east_west
    return abs(area)

def area_of_walls(path):
    return len(path) // 2 - 1

def enclosed_area(path):
    return area_of_path(path) - area_of_walls(path)

grid = []
for line in open(sys.argv[1], 'r'):
    grid.append(line.strip())

for row in grid:
    print(row)

start_loc = None
for (r, row) in enumerate(grid):
    for (c, cell) in enumerate(row):
        if cell == "S":
            start_loc = (r, c)
print("Start location:", start_loc)

(start_row, start_col) = start_loc
for direction in DIRECTIONS:
    path = follow_pipe(grid, start_row, start_col, direction)
    if path is not None:
        print("Path:", path)
        print("Length:", len(path))
        print("Path area:", area_of_path(path))
        print("Wall area:", area_of_walls(path))
        print("Enclosed area:", enclosed_area(path))
        sys.exit(1)

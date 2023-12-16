import sys

DIRECTIONS = {
    "R": (0, +1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (+1, 0)
}

MIRRORS = {
    ".": {
        "R": "R",
        "L": "L",
        "D": "D",
        "U": "U"
    },
    "\\": {
        "R": "D",
        "L": "U",
        "D": "R",
        "U": "L",
    },
    "/": {
        "R": "U",
        "L": "D",
        "D": "L",
        "U": "R",
    },
    "-": {
        "R": "R",
        "L": "L",
        "D": "LR",
        "U": "LR",
    },
    "|": {
        "R": "UD",
        "L": "UD",
        "D": "D",
        "U": "U",
    }
}

def display(grid):
    for row in grid:
        print("".join(row))

def is_valid(grid, row, col):
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])

def split_beam(grid, beam):
    (direction, row, col) = beam
    obj = grid[row][col]
    for new_direction in MIRRORS[obj][direction]:
        (delta_row, delta_col) = DIRECTIONS[new_direction]
        (new_row, new_col) = (row + delta_row, col + delta_col)
        if is_valid(grid, new_row, new_col):
            yield(new_direction, new_row, new_col)

def fill(grid, start_beam):
    beams = set()
    frontier = [start_beam]
    while len(frontier) > 0:
        beam = frontier.pop()
        if beam not in beams:
            beams.add(beam)
        for beam in split_beam(grid, beam):
            if beam not in beams and beam not in frontier:
                frontier.append(beam)
    return beams

def beam_count(beams):
    return len({(row, col) for (_, row, col) in beams})

grid = []
for line in open(sys.argv[1], 'r'):
    grid.append([ch for ch in line.strip()])

height = len(grid)
width = len(grid[0])
starting_options = (
    [("R", row, 0) for row in range(height)]
    + [("L", row, width - 1) for row in range(height)]
    + [("D", 0, col) for col in range(width)]
    + [("U", height - 1, col) for col in range(width)]
)

display(grid)
max_energy = 0
for start in starting_options:
    energy = beam_count(fill(grid, start))
    max_energy = max(energy, max_energy)
    print("energy:", energy)
print("Max energy:", max_energy)

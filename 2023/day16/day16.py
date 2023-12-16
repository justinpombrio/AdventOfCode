import sys

def display(grid):
    for row in grid:
        print("".join(row))

def valid(grid, beam):
    (_, row, col) = beam
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])

def next(grid, beam):
    (direction, row, col) = beam
    obj = grid[row][col]
    if obj == ".":
        if direction == "R":
            return [("R", row, col + 1)]
        elif direction == "L":
            return [("L", row, col - 1)]
        elif direction == "D":
            return [("D", row + 1, col)]
        elif direction == "U":
            return [("U", row - 1, col)]
    elif obj == "\\":
        if direction == "R":
            return [("D", row + 1, col)]
        elif direction == "L":
            return [("U", row - 1, col)]
        elif direction == "D":
            return [("R", row, col + 1)]
        elif direction == "U":
            return [("L", row, col - 1)]
    elif obj == "/":
        if direction == "R":
            return [("U", row - 1, col)]
        elif direction == "L":
            return [("D", row + 1, col)]
        elif direction == "D":
            return [("L", row, col - 1)]
        elif direction == "U":
            return [("R", row, col + 1)]
    elif obj == "-":
        if direction == "R":
            return [("R", row, col + 1)]
        elif direction == "L":
            return [("L", row, col - 1)]
        elif direction == "D" or direction == "U":
            return [("R", row, col + 1), ("L", row, col - 1)]
    elif obj == "|":
        if direction == "L" or direction == "R":
            return [("U", row - 1, col), ("D", row + 1, col)]
        elif direction == "D":
            return [("D", row + 1, col)]
        elif direction == "U":
            return [("U", row - 1, col)]
    raise "oops"

def fill(grid, start):
    beams = {}
    frontier = [start]
    while len(frontier) > 0:
        beam = frontier.pop()
        if beam not in beams:
            beams[beam] = 1
        for beam in next(grid, beam):
            if valid(grid, beam) and beam not in beams and beam not in frontier:
                frontier.append(beam)
    return beams

def energy(grid, start):
    beams = fill(grid, start)
    energy = {}
    for beam in beams:
        (_, row, col) = beam
        energy[(row, col)] = 1
    return len(energy)

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
    n = energy(grid, start)
    max_energy = max(n, max_energy)
    print("energy:", n)
print("Max energy:", max_energy)

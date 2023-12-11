import sys

EXPANSION_RATE = 1000000

space = []
for line in open(sys.argv[1], 'r'):
    space.append(line.strip())

expanding_rows = [
    row for row in range(len(space))
    if all(map(lambda c: c == ".", space[row]))
]

expanding_cols = [
    col for col in range(len(space[0]))
    if all(map(lambda c: c == ".", [space[row][col] for row in range(len(space))]))
]

galaxies = [
    (row, col)
    for row in range(len(space))
    for col in range(len(space[0]))
    if space[row][col] == "#"
]

def distance(galaxy1, galaxy2, expanding_rows, expanding_cols):
    (row1, col1) = galaxy1
    (row2, col2) = galaxy2
    dist = 0
    for row in range(min(row1, row2), max(row1, row2)):
        dist += EXPANSION_RATE if row in expanding_rows else 1
    for col in range(min(col1, col2), max(col1, col2)):
        dist += EXPANSION_RATE if col in expanding_cols else 1
    print(" ", galaxy1, "->", galaxy2, "=", dist)
    return dist

def total_distance(galaxies, expanding_rows, expanding_cols):
    dist = 0
    for (i, galaxy1) in enumerate(galaxies):
        for galaxy2 in galaxies[i + 1:]:
            dist += distance(galaxy1, galaxy2, expanding_rows, expanding_cols)
    return dist

print("Expanding rows:", expanding_rows)
print("Expanding cols:", expanding_cols)
print("Galaxies:", galaxies)
print("Total distance:", total_distance(galaxies, expanding_rows, expanding_cols))

import sys

grid = []
for line in open(sys.argv[1], 'r'):
    grid.append([ch for ch in line.strip()])

while True:
    found = False
    for r in range(len(grid)):
        if found:
            break
        for c in range(len(grid[0])):
            cell_above = grid[r][c]
            cell_below = grid[r + 1][c]
            if cell_above == "." and cell_below == "O":
                grid[r][c] = "O"
                grid[r + 1][c] = "."
                found = True
                break
    if not found:
        break

def count(grid):
    total = 0
    for (i, row) in enumerate(reversed(grid)):
        for cell in row:
            if cell == "O":
                total += i + 1
    return total

for line in grid:
    print("".join(line))

print("Total:", count(grid))

import sys

grid = []
start = set()
for (r, line) in enumerate(open(sys.argv[1], 'r')):
    row = []
    for (c, ch) in enumerate(line.strip()):
        if ch == "S":
            start.add((r, c))
            row.append(".")
        elif ch == ".":
            row.append(".")
        elif ch == "#":
            row.append("#")
        else:
            raise "bad"
    grid.append(row)

def valid(grid, r, c):
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0])

def neighbors(r, c):
    yield (r - 1, c)
    yield (r + 1, c)
    yield (r, c - 1)
    yield (r, c + 1)

def one_step(r, c):
    for r, c in neighbors(r, c):
        if valid(grid, r, c) and grid[r][c] == ".":
            yield r, c

def reachable(steps, positions):
    while steps > 0:
        if steps % 10 == 0:
            print("steps:", steps, "count:", len(positions))
        new_positions = set()
        for r, c in positions:
            for pos in one_step(r, c):
                new_positions.add(pos)
        positions = new_positions
        steps -= 1
    return positions

for row in grid:
    print("".join(row))

positions = reachable(64, start)
print(len(positions))

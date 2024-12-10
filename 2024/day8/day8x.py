from sys import stdin

grid = []
for line in stdin:
    grid.append([ch for ch in line.strip()])

nodes = {} # freq to (x, y)
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] != ".":
            freq = grid[y][x]
            if freq not in nodes:
                nodes[freq] = []
            nodes[freq].append((x, y))

def valid(coords):
    (x, y) = coords
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def print_grid():
    for line in grid:
        print("".join(line))

antinodes = {}
for freq in nodes:
    freq_nodes = nodes[freq]
    antinodes[freq] = []
    freq_antinodes = antinodes[freq]
    for i in range(len(freq_nodes)):
        for j in range(i+1, len(freq_nodes)):
            (x1, y1), (x2, y2) = freq_nodes[i], freq_nodes[j]
            (dx, dy) = (x1 - x2, y1 - y2)
            (x, y) = (x1, y1)
            while valid((x, y)):
                freq_antinodes.append((x, y))
                (x, y) = (x + dx, y + dy)
            (x, y) = (x2, y2)
            while valid((x, y)):
                freq_antinodes.append((x, y))
                (x, y) = (x - dx, y - dy)

for freq in antinodes:
    for (x, y) in antinodes[freq]:
        grid[y][x] = "#"

num_unique_antinodes = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == "#":
            num_unique_antinodes += 1

print_grid()
print()
print("Nodes:", nodes)
print()
print("Antinodes:", antinodes)
print()
print_grid()
print()
print("Total:", num_unique_antinodes)

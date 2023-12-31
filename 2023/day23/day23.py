import sys

def valid(grid, r, c):
    return r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0])

def reachable_neighbors(grid, r, c):
    if valid(grid, r - 1, c) and grid[r - 1][c] != "#":# in ".^":
        yield (r - 1, c)
    if valid(grid, r + 1, c) and grid[r + 1][c] != "#":# in ".v":
        yield (r + 1, c)
    if valid(grid, r, c - 1) and grid[r][c - 1] != "#":# in ".<":
        yield (r, c - 1)
    if valid(grid, r, c + 1) and grid[r][c + 1] != "#":# in ".>":
        yield (r, c + 1)

def extend_path(grid, path):
    (r, c) = path[-1]
    for next_pos in reachable_neighbors(grid, r, c):
        if next_pos not in path:
            yield path + [next_pos]

def longest_path(grid, start, end):
    longest_len = 0
    frontier = [[start]]
    while len(frontier) > 0:
        path = frontier.pop()
        for new_path in extend_path(grid, path):
            frontier.append(new_path)
            length = len(new_path) - 1
            if new_path[-1] == end and length > longest_len:
                longest_len = length
                print("length:", longest_len, "frontier:", len(frontier))
    return longest_len

grid = []
for line in open(sys.argv[1], 'r'):
    grid.append(list(line.strip()))
start = (0, 1)
end = (len(grid) - 1, len(grid[0]) - 2)

print(grid)
longest = longest_path(grid, start, end)
print("LONGEST PATH:", longest)

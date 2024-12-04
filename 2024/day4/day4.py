from sys import stdin

grid = []
for line in stdin:
    grid.append([ch for ch in line.strip()])

def words(grid):
    for x in range(len(grid) - 3):
        for y in range(len(grid)):
            yield grid[x][y] + grid[x+1][y] + grid[x+2][y] + grid[x+3][y]
    for x in range(len(grid)):
        for y in range(len(grid) - 3):
            yield grid[x][y] + grid[x][y+1] + grid[x][y+2] + grid[x][y+3]
    for x in range(len(grid) - 3):
        for y in range(len(grid) - 3):
            yield grid[x][y] + grid[x+1][y+1] + grid[x+2][y+2] + grid[x+3][y+3]
            yield grid[x+3][y] + grid[x+2][y+1] + grid[x+1][y+2] + grid[x][y+3]

count = len([word for word in words(grid) if word == "XMAS" or word == "SAMX"])
print(count)

from sys import stdin

grid = []
for line in stdin:
    grid.append([ch for ch in line.strip()])

def words(grid):
    for x in range(len(grid) - 2):
        for y in range(len(grid) - 2):
            word_1 = grid[x][y] + grid[x+1][y+1] + grid[x+2][y+2]
            word_2 = grid[x+2][y] + grid[x+1][y+1] + grid[x][y+2]
            yield (word_1, word_2)

count = len([
    None for (w1, w2) in words(grid)
    if (w1 == "MAS" or w1 == "SAM") and (w2 == "MAS" or w2 == "SAM")])
print(count)

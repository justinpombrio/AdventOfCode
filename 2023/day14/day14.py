import sys

def roll(grid):
    while True:
        found = False
        for r in range(len(grid)):
            if found:
                break
            for c in range(len(grid[0])):
                if grid[r][c] == "O":
                    r_move_to = None
                    for r_above in range(r - 1, -1, -1):
                        if grid[r_above][c] == ".":
                            r_move_to = r_above
                        else:
                            break
                    if r_move_to is not None:
                        grid[r_move_to][c] = "O"
                        grid[r][c] = "."
                        #print("swap", r, c, r_move_to, c)
                        found = True
                        #for line in grid:
                        #    print("".join(line))
                        #print()
                        break
        if not found:
            break

def rotate(grid):
    new_grid = [["?" for cell in row] for row in grid]
    width = len(grid[0])
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            new_grid[r][c] = grid[width - c - 1][r]
    return new_grid

def count(grid):
    total = 0
    for (i, row) in enumerate(reversed(grid)):
        for cell in row:
            if cell == "O":
                total += i + 1
    return total

def display(grid):
    for line in grid:
        print("".join(line))
    print()

def same(grid1, grid2):
    for r in range(len(grid1)):
        for c in range(len(grid1[0])):
            if grid1[r][c] != grid2[r][c]:
                return False
    return True

grid = []
for line in open(sys.argv[1], 'r'):
    grid.append([ch for ch in line.strip()])
assert len(grid) == len(grid[0])

roll(grid)
display(grid)

grids = [grid]
for i in range(1, 1000000):
    grid = rotate(grid)
    roll(grid)
    # normalized_grid = grid
    # for _ in range(4 - i % 4):
    #     normalized_grid = rotate(normalized_grid)
    # weight = count(normalized_grid)
    # display(normalized_grid)
    print("Step:", i)
    # print("Weight:", weight)
    print()
    for (j, g) in enumerate(grids):
        if same(grid, g) and i % 4 == 3 and j % 4 == 3:
            print("Cycle from", i, "to", j)
            k = i + (1000000000 * 4 - 1 - i) % (j - i)
            print("Solution is at", k)
            normalized_grid = grids[k]
            for _ in range(4 - k % 4):
                normalized_grid = rotate(normalized_grid)
            weight = count(normalized_grid)
            print("Weight:", weight)
            sys.exit(1)
    grids.append(grid)

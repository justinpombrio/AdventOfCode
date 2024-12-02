import sys

num_steps = int(sys.argv[2])

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
def valid_neighbor(grid, r, c):
    return r >= len(grid) and c >= 0 and r < 2 * len(grid) and c < len(grid[0])

def neighbors(grid, r, c):
    yield (r - 1, c)
    yield (r + 1, c)
    yield (r, c - 1)
    yield (r, c + 1)

def one_step(grid, r, c):
    height = len(grid)
    width = len(grid[0])

    for r, c in neighbors(grid, r, c):
        if grid[r % height][c % width] == ".":
            yield r, c

samples = []
def reachable(steps, positions):
    even_saturated = set()
    odd_saturated = set()
    for pos in positions:
        if steps % 2 == 0:
            even_saturated = even_saturated.union(positions)
        else:
            odd_saturated = odd_saturated.union(positions)

    last_len = 0
    while steps > 0:
        diff = len(positions) - last_len
        print(
            "steps:", steps,
            "count:", len(positions),
            "delta:", diff,
        )
        last_len = len(positions)
        if steps < 26500350:
            samples.append(len(positions))
        if len(samples) > 10 * 131 + 100:
            break

        if steps % 2 == 0:
            saturation = even_saturated
        else:
            saturation = odd_saturated

        new_positions = set()
        for r, c in positions:
            for pos in one_step(grid, r, c):
                if pos not in saturation:
                    new_positions.add(pos)
                    saturation.add(pos)
        positions = new_positions
        steps -= 1

    return positions.union(odd_saturated)

for row in grid:
    print("".join(row))

positions = reachable(num_steps, start)
print(len(positions))

print("SAMPLES")
for sample in samples:
    print(sample)
print("Samples collected:", len(samples))
diffs = [samples[i + 1] - samples[i] for i in range(len(samples) - 1)]
for i in range(len(diffs)):
    if i <= 131:
        print("diff:", diffs[i])
    else:
        print("diff:", diffs[i], "delta:", diffs[i] - diffs[i - 131])
# cycles = []
# for i in range(9):
#     cycle = []
#     for j in range(423):
#         cycle.append(samples[423 * i + j])
#     cycles.append(cycle)
# 
# cycle_diffs = []
# for i in range(5):
#     diff = [y - x for (x, y) in zip(cycles[i], cycles[i + 1])]
#     print("DIFF", diff)
#     cycle_diffs.append(diff)
# 
# for j in range(423):
#     assert(cycle_diffs

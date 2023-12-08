import sys
import re
import math
import functools

# This solution relies on the fact that if you can get from a start location
# to an end location in N steps, it also goes to that end location in K*N steps
# for every K. This is a very strong, unjustified assumption! Why did they give
# us an input for which it holds?

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

turns = []
road_map = {}
for line in open(sys.argv[1], 'r'):
    line = line.strip()
    road_match = re.search("([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)", line)
    if line == "":
        continue
    elif road_match:
        road_map[road_match.group(1)] = (road_match.group(2), road_match.group(3))
    else:
        turns = line

locations = [loc for loc in road_map if loc.endswith("A")]
cycle_lens = []
for loc in locations:
    print(loc)
    steps = 0
    done = False
    while not done:
        for turn in turns:
            loc = road_map[loc][0 if turn == "L" else 1]
            steps += 1
            print("  ->", loc)
            if loc.endswith("Z"):
                print("Cycle len:", steps)
                done = True
                cycle_lens.append(steps)

print("Cycle Lengths:", cycle_lens)
total = functools.reduce(lcm, cycle_lens, 1)
print("Total Distance:", total)

import sys
import math

with open(sys.argv[1], 'r') as file:
    lines = file.read().split("\n")
    time = int("".join(lines[0].split()[1:]))
    dist = int("".join(lines[1].split()[1:]))

ways_to_win_race = 0
for charge in range(time):
    achieved_dist = (time - charge) * charge
    if achieved_dist > dist:
        ways_to_win_race += 1

print("possibilities:", ways_to_win_race)

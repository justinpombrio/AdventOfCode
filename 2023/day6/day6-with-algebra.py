import sys
from math import floor, ceil, sqrt

with open(sys.argv[1], 'r') as file:
    lines = file.read().split("\n")
    time = int("".join(lines[0].split()[1:]))
    dist = int("".join(lines[1].split()[1:]))
    # Use the quadratic formula to determine the min & max winning charge
    # (dist = charge * (time - charge))
    min_charge = (time - sqrt(time * time - 4 * dist)) / 2.0
    max_charge = (time + sqrt(time * time - 4 * dist)) / 2.0
    # Now round to integer solutions, keeping in mind that we need to _beat_ the record
    min_charge_int = floor(min_charge + 1)
    max_charge_int = ceil(max_charge - 1)
    # The answer is the total number of winning charges
    print("Ways to win:", max_charge_int - min_charge_int + 1)

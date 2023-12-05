import sys
import re

# Keep track of the current sets of objects in lists of ranges:
# prev_ranges is from last iteration and next_ranges is the new objects.
prev_ranges = []
next_ranges = []
for line in open(sys.argv[1], 'r'):
    line = line.strip()
    if line == "": continue

    seeds_match = re.search("seeds:(.*)", line)
    if seeds_match:
        seed_input = list(map(int, seeds_match.group(1).split()))
        for i in range(len(seed_input) // 2):
            next_ranges.append((seed_input[2 * i], seed_input[2 * i] + seed_input[2 * i + 1]))
        print("seeds:", next_ranges)

    heading_match = re.search("([a-z]+)-to-([a-z]+) map:", line)
    if heading_match:
        source = heading_match.group(1)
        dest = heading_match.group(2)
        prev_ranges = prev_ranges + next_ranges # unmapped objects keep their number
        next_ranges = []
        print(source, "->", dest)
        print(prev_ranges)

    mapping_match = re.search("^([0-9]+) ([0-9]+) ([0-9]+)", line)
    if mapping_match:
        dst_start = int(mapping_match.group(1))
        src_start = int(mapping_match.group(2))
        length = int(mapping_match.group(3))
        (x0, x1, delta) = (src_start, src_start + length, dst_start - src_start)

        # Split out the sub-range that the mapping applies to.
        leftover_ranges = []
        for (y0, y1) in prev_ranges:
            (z0, z1) = (y0, min(y1, x0))
            if z1 > z0:
                leftover_ranges.append((z0, z1))
            (z0, z1) = (max(y0, x1), y1)
            if z1 > z0:
                leftover_ranges.append((z0, z1))
            (z0, z1) = (max(y0, x0), min(y1, x1))
            if z1 > z0:
                next_ranges.append((z0 + delta, z1 + delta))
        prev_ranges = leftover_ranges

final_ranges = prev_ranges + next_ranges
print("Min location:", min([x for (x, y) in final_ranges]))

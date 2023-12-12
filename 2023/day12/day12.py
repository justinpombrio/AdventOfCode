import sys

def can_be_empty(record):
    return all(map(lambda spring: spring in ".?", record))

def place_broken_seq(record, group, start):
    end = start + group
    for i in range(start, end):
        if i >= len(record) or record[i] not in "#?":
            return None

    if start == 0:
        before = ""
    elif record[start - 1] == "#":
        return None
    else:
        before = record[:start - 1]

    if end == len(record):
        after = ""
    elif record[end] == "#":
        return None
    else:
        after = record[end + 1:]

    return (before, after)

def sensible_placements(record, left_groups, center_group, right_groups):
    min_left_len = sum(left_groups) + len(left_groups) - 1
    min_right_len = sum(right_groups) + len(right_groups) - 1
    for i in range(max(0, min_left_len), len(record) - min_right_len - center_group):
        yield i

def count(record, groups):
    # If we've placed all the groups already, make sure the row is empty.
    if len(groups) == 0:
        return 1 if can_be_empty(record) else 0

    # We're going to place the middle group. First pull it out.
    middle_index = len(groups) // 2
    left_groups = groups[:middle_index]
    center_group = groups[middle_index]
    right_groups = groups[middle_index + 1:]

    # Now try placing it at each location.
    total = 0
    for placement in sensible_placements(record, left_groups, center_group, right_groups):
        result = place_broken_seq(record, center_group, placement)
        if result is not None:
            (before, after) = result
            before_count = count(before, left_groups)
            if before_count != 0:
                total += before_count * count(after, right_groups)
    return total

total = 0
for i, line in enumerate(open(sys.argv[1], 'r')):
    record, groups = line.strip().split()
    record = "?".join([record] * 5)
    groups = list(map(int, groups.split(","))) * 5

    num_arrangements = count(record, groups)
    total += num_arrangements
    print(i)
    print(record)
    print(groups)
    print("->", num_arrangements)
    print()

print("Total:", total)

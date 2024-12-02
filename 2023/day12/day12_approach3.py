import sys

def organize_record(record):
    segments = []
    last_spring = None
    for spring in record:
        if spring == last_spring:
            count = segments[-1][1]
            segments[-1] = (last_spring, count + 1)
        else:
            segments.append((spring, 1))
        last_spring = spring
    return segments

def split_record(record):
    assert len(record) > 1
    middle_index = len(record) // 2
    head = record[:middle_index]
    left = record[middle_index]
    right = record[middle_index + 1]
    tail = record[middle_index + 1:]
    if left[0] == "?":
        return (head + [left], right, tail)
    else:
        return (head, left, [right] + tail)

def group_splits(group):
    for i in range(len(group)):
        yield (group[:i], group[i:])

def count(record, groups, extending, separating):
    global depth
    depth += 1
    result = inner_count(row, groups, extending, separating)
    #print(" " * depth, row, groups, extending, "->", result)
    depth -= 1
    return result

def inner_count(row, groups, extending, separating):
    if groups and groups[0] == 0 and extending:
        groups = groups[1:]
        extending = False
        separating = True
    if len(row) == 0:
        return 1 if sum(groups) == 0 else 0
    if row[0] == ".":
        return count(row[1:], groups, False, False)
    elif row[0] == "#" or extending:
        if len(groups) == 0 or separating:
            return 0
        return count(row[1:], [groups[0] - 1] + groups[1:], True, False)
    else:
        total = count(row[1:], groups, False, False)
        if len(groups) != 0 and not separating:
            total += count(row[1:], [groups[0] - 1] + groups[1:], True, False)
        return total

total = 0
for line in open(sys.argv[1], 'r'):
    record, groups = line.strip().split()
    orig_record = record * 5
    record = organize_record(record)
    groups = list(map(int, groups.split(","))) * 5

    num_arrangements = 1
    total += num_arrangements
    print(orig_record)
    print(groups, "->", num_arrangements)
    print()

print("Total:", total)

import sys

depth = 0
def count(row, groups, extending, separating):
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
    groups = list(map(int, groups.split(",")))

    record = record * 5
    groups = groups * 5

    num_arrangements = count(record, groups, False, False)
    total += num_arrangements
    print("  " + record, groups, "->", num_arrangements)
    print()

print("Total:", total)

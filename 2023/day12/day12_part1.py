import sys

def matches(record, row):
    for i in range(len(record)):
        expected = record[i]
        actual = row[i]
        if expected != "?" and expected != actual:
            return False
    return True

def possible_rows(groups, length):
    if len(groups) == 0:
        return ["." * length]
    if sum(groups) > length:
        return []
    first_group = groups[0]
    remaining_groups = groups[1:]
    rows = [
        "#" * first_group + "." + row
        for row in possible_rows(remaining_groups, length - first_group - 1)
    ]
    rows += [
        "." + row
        for row in possible_rows(groups, length - 1)
    ]
    return rows

total = 0
for line in open(sys.argv[1], 'r'):
    record, groups = line.strip().split()
    record = record + "."
    groups = list(map(int, groups.split(",")))
    rows = possible_rows(groups, len(record))
    num_matches = 0
    print("   ", record)
    for row in rows:
        print("   ", row, matches(record, row))
        if matches(record, row):
            num_matches += 1
    print(num_matches)
    total += num_matches

print("Total:", total)

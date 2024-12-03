from sys import stdin

def differences(seq):
    return [
        seq[i + 1] - seq[i]
        for i in range(len(seq) - 1)
    ]

def is_safe(report):
    diffs = differences(report)
    if diffs[0] < 0:
        diffs = [-1 * diff for diff in diffs]
    return all(map(lambda n: 1 <= n <= 3, diffs))

# All reports that differ from `report` by removing a single level.
def shrinkages(report):
    for i in range(len(report)):
        yield report[:i] + report[i+1:]

def is_safe_with_dampener(report):
    return any([is_safe(shrunk) for shrunk in shrinkages(report)])

reports = []
for line in stdin:
    reports.append([int(s) for s in line.strip().split()])

num_safe = 0
for report in reports:
    print("Report", report)
    print("  differences", differences(report))
    print("  shrinkages", list(shrinkages(report)))
    print("  immediately safe?", is_safe(report))
    print("  is safe with dampener?", is_safe_with_dampener(report))
    if is_safe_with_dampener(report):
        num_safe += 1
print("num safe", num_safe)

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

reports = []
for line in stdin:
    reports.append([int(s) for s in line.strip().split()])

num_safe = 0
for report in reports:
    print("report", report)
    print("differences", differences(report))
    print("safe?", is_safe(report))
    if is_safe(report):
        num_safe += 1
print("num safe", num_safe)

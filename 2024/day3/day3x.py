from sys import stdin
import re

regex = "mul\(([0-9][0-9]?[0-9]?),([0-9][0-9]?[0-9]?)\)|(do)\(\)|(don't)\(\)"

total = 0
enabled = True
for line in stdin:
    for match in re.findall(regex, line):
        if match[2] == "do":
            enabled = True
        elif match[3] == "don't":
            enabled = False
        elif enabled and match[0] != "":
            total += int(match[0]) * int(match[1])

print("total", total)

from sys import stdin
import re

total = 0
for line in stdin:
    for match in re.findall("mul\(([0-9][0-9]?[0-9]?),([0-9][0-9]?[0-9]?)\)", line):
        product = int(match[0]) * int(match[1])
        total += product
print("total", total)


import sys

def hash(string):
    v = 0
    for ch in string:
        v += ord(ch)
        v = 17 * v
        v = v % 256
    return v

steps = []
for line in open(sys.argv[1], 'r'):
    steps = list(line.strip().split(","))

total = 0
for step in steps:
    print(step, hash(step))
    total += hash(step)
print(total)


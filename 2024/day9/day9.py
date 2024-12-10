from sys import stdin

for line in stdin:
    disk_map = [int(ch) for ch in line.strip()]
layout = []
next_id = 0
for i in range(len(disk_map)):
    if i % 2 == 1:
        for _ in range(disk_map[i]):
            layout.append(".")
    else:
        for _ in range(disk_map[i]):
            layout.append(str(next_id))
        next_id += 1

def show(seq):
    return "".join([str(n) for n in seq])

def checksum(seq):
    total = 0
    for i in range(len(seq)):
        total += i * int(seq[i])
    return total

print(show(disk_map))

print(show(layout))
step = 0
while "." in layout:
    if layout[-1] == ".":
        layout = layout[:-1]
    i = layout.index(".")
    layout[i] = layout[-1]
    layout = layout[:-1]
    if step % 1000 == 0:
        print(show(layout))
        print("step", step)
    step += 1

print("checksum", checksum(layout))

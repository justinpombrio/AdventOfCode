from sys import stdin

for line in stdin:
    disk_map = [int(ch) for ch in line.strip()]

layout = []
next_id = 0
for i in range(len(disk_map)):
    if i % 2 == 1:
        layout.append((".", disk_map[i]))
    else:
        layout.append((next_id, disk_map[i]))
        next_id += 1

def show(seq):
    s = ""
    for (id, len) in seq:
        s += (str(id) + ",") * len + "|"
    return s

def checksum(seq):
    total = 0
    i = 0
    for (id, len) in seq:
        for _ in range(len):
            total += 0 if id == "." else i * id
            i += 1
    return total

print(show(layout))

step = 0
for id in reversed(range(next_id)):
    j = next(i for i, pair in enumerate(layout) if pair[0] == id)
    for i in range(j):
        if layout[i][0] == "." and layout[j][1] <= layout[i][1]:
            layout[i] = (layout[i][0], layout[i][1] - layout[j][1])
            layout.insert(i, layout[j])
            layout[j+1] = (".", layout[j+1][1])
            break
    if step % 1000 == 0:
        print(show(layout))
        print("step", step)
    step += 1

print("checksum", checksum(layout))

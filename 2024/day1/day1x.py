from sys import stdin

list_a = []
list_b = []

for line in stdin:
    (elem_a, elem_b) = line.strip().split()
    list_a.append(int(elem_a))
    list_b.append(int(elem_b))

score = 0
for a in list_a:
    for b in list_b:
        if a == b:
            score += a
print(score)

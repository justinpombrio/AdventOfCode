from sys import stdin

list_a = []
list_b = []

for line in stdin:
    (elem_a, elem_b) = line.strip().split()
    list_a.append(int(elem_a))
    list_b.append(int(elem_b))

list_a.sort()
list_b.sort()

score = 0
for (a, b) in zip(list_a, list_b):
    score += abs(a - b)
print(score)

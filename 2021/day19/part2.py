coords = []
for line in open("x.txt", "r"):
    parts = line.strip().split(" ")
    x = int(parts[2][1:-1])
    y = int(parts[3][:-1])
    z = int(parts[4][:-1])
    print (x, y, z)
    coords.append((x, y, z))

max_dist = 0
for c1 in coords:
    for c2 in coords:
        (x, y, z) = c1
        (x2, y2, z2) = c2
        d = abs(x - x2) + abs(y - y2) + abs(z - z2)
        max_dist = max(max_dist, d)
print "max dist", max_dist

import sys

#RANGE = 7.0, 27.0
RANGE = 200000000000000.0, 400000000000000.0

def intersection(stone1, stone2):
    ((x1, y1, z1), (dx1, dy1, dz1)) = stone1
    (x2, y2, z2) = (x1 + dx1, y1 + dy1, z1 + dz1)
    ((x3, y3, z3), (dx3, dy3, dz3)) = stone2
    (x4, y4, z4) = (x3 + dx3, y3 + dy3, z3 + dz3)
    denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    numer_x = (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
    numer_y = (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)
    if denom == 0.0:
        return (1e50, 1e50);
    return (numer_x / denom, numer_y / denom)

def is_forward_in_time(pos, stone):
    xi, yi = pos
    (x, y, z), (dx, dy, dz) = stone
    return xi > x and dx > 0 or xi < x and dx < 0

hailstones = []
for line in open(sys.argv[1], 'r'):
    pos_str, vel_str = line.strip().split(" @ ")
    x, y, z = pos_str.split(", ")
    x, y, z = float(x), float(y), float(z)
    dx, dy, dz = vel_str.split(", ")
    dx, dy, dz = float(dx), float(dy), float(dz)
    hailstones.append(((x, y, z), (dx, dy, dz)))

total = 0
for i in range(len(hailstones)):
    for j in range(i + 1, len(hailstones)):
        stone_1 = hailstones[i]
        stone_2 = hailstones[j]
        x, y = intersection(stone_1, stone_2)
        in_range = x >= RANGE[0] and y >= RANGE[0] and x <= RANGE[1] and y <= RANGE[1]
        is_forward = is_forward_in_time((x, y), stone_1) and is_forward_in_time((x, y), stone_2)
        print(i, j, "intersects", x, y, "->", in_range, "forward?", is_forward)
        if in_range and is_forward:
            total += 1
print("Total:", total)

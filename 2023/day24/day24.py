import sys

def stone_at(stone, time):
    (x, y, z), (dx, dy, dz) = stone
    return (x + dx * time, y + dy * time, z + dz * time)

def intersection(stone1, stone2):
    ((x1, y1, z1), (dx1, dy1, dz1)) = stone1
    ((x2, y2, z2), (dx2, dy2, dz2)) = stone2
    if dx2 - dx1 == 0:
        return None
    t = (x1 - x2) // (dx2 - dx1)
    if stone_at(stone1, t) == stone_at(stone2, t):
        return stone_at(stone1, t)
    else:
        return None

def diff(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return x1 - x2, y1 - y2, z1 - z2

def div(pos, t):
    x, y, z = pos
    rx, ry, rz = x//t, y//t, z//t
    if (rx*t, ry*t, rz*t) == (x, y, z):
        return rx, ry, rz
    else:
        return None

def is_forward_in_time(pos, stone):
    xi, yi, zi = pos
    (x, y, z), (dx, dy, dz) = stone
    return xi > x and dx > 0 or xi < x and dx < 0

hailstones = []
for line in open(sys.argv[1], 'r'):
    pos_str, vel_str = line.strip().split(" @ ")
    x, y, z = pos_str.split(", ")
    x, y, z = int(x), int(y), int(z)
    dx, dy, dz = vel_str.split(", ")
    dx, dy, dz = int(dx), int(dy), int(dz)
    hailstones.append(((x, y, z), (dx, dy, dz)))

total = 0
for i in range(len(hailstones)):
    print(i, "/", len(hailstones))
    for j in range(len(hailstones)):
        if i == j:
            continue
        stone_1 = hailstones[i]
        stone_2 = hailstones[j]
        pos_1 = stone_at(stone_1, 1)

        for dt in range(1, 10000):
            pos_2 = stone_at(stone_2, 1 + dt)
            vel = div(diff(pos_2, pos_1), dt)
            if vel is None:
                continue
            pos_0 = diff(pos_1, vel)
            rock = (pos_0, vel)
            #print("Trying rock:", rock, "for", i, j)

            works = True
            for k in range(len(hailstones)):
                if k == i or k == j:
                    continue
                if intersection(hailstones[k], rock) is None:
                    works = False
            if works:
                print("Success!", rock)
                x, y, z = pos_0
                print("sum:", x + y + z)
                sys.exit(1)

print("Failure :-(")

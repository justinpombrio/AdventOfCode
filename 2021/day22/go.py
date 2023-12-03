filename = "input.txt"

instructions = []
for line in open(filename, "r"):
    outer = line.strip().split(" ")
    if outer[0] == "on":
        on = True
    elif outer[0] == "off":
        on = False
    else:
        raise "oops"
    parts = outer[1].split(",")
    x_parts = parts[0][2:].split("..")
    y_parts = parts[1][2:].split("..")
    z_parts = parts[2][2:].split("..")
    x_range = int(x_parts[0]), int(x_parts[1])
    y_range = int(y_parts[0]), int(y_parts[1])
    z_range = int(z_parts[0]), int(z_parts[1])
    instructions.append((on, x_range, y_range, z_range))

def range_intersection((x0, x1), (X0, X1)):
    left = max(x0, X0)
    right = min(x1, X1)
    if left <= right:
        return (left, right)
    else:
        return None

def intersection(cube, Cube):
    (x, y, z) = cube
    (X, Y, Z) = Cube
    xi = range_intersection(x, X)
    yi = range_intersection(y, Y)
    zi = range_intersection(z, Z)
    if xi is None or yi is None or zi is None:
        return None
    return (xi, yi, zi)

cubes = []
neg_cubes = []
def insert(new_cube):
    global cubes
    global neg_cubes
    (on, x, y, z) = new_cube
    # subtract all intersections
    new_neg_cubes = []
    for cube in cubes:
        i = intersection((x, y, z), cube)
        if i is not None:
            new_neg_cubes.append(i)
    for neg_cube in neg_cubes:
        i = intersection((x, y, z), neg_cube)
        if i is not None:
            cubes.append(i)
    neg_cubes.extend(new_neg_cubes)
    if on:
        # add new_cube
        cubes.append((x, y, z))
    optimize()

def optimize():
    global cubes
    global neg_cubes
    shared = [cube for cube in cubes if cube in neg_cubes]
    cubes = [cube for cube in cubes if cube not in shared]
    neg_cubes = [cube for cube in neg_cubes if cube not in shared]

def range_len((a, b)):
    return b + 1 - a

def size(cube):
    (x, y, z) = cube
    return range_len(x) * range_len(y) * range_len(z)

def count_cubes():
    count = 0
    for cube in cubes:
        count += size(cube)
    for cube in neg_cubes:
        count -= size(cube)
    return count

for (i, new_cube) in enumerate(instructions):
    print ""
    print "instruction", i, new_cube
    (_, x, y, z) = new_cube
    insert(new_cube)
    print "count", count_cubes()
    print "num cubes", len(cubes), len(neg_cubes)
    #print "pos cubes"
    #for cube in cubes: print cube
    #print "neg cubes"
    #for cube in neg_cubes: print cube

count = count_cubes()
print "final count", count

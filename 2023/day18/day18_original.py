import sys

DIRECTION_CODES = "RDLU"

DIRECTIONS = {
    "R": (0, +1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (+1, 0)
}

def area_of_path(path):
    area = 0
    left_right = 0
    for direction in path:
        if direction == "R":
            left_right += 1
        elif direction == "L":
            left_right -= 1
        elif direction == "U":
            area += left_right
        elif direction == "D":
            area -= left_right
    return abs(area)

def area_of_walls(path):
    return len(path) // 2 - 1

def enclosed_area(path):
    return area_of_path(path) - area_of_walls(path)

def total_area(path):
    return area_of_path(path) - area_of_walls(path) + len(path)

loc = (0, 0)
path = []
for line in open(sys.argv[1], 'r'):
    (_direction, _length, code) = line.strip().split()
    length = int("0x" + code[2:7], 0)
    direction = DIRECTION_CODES[int(code[7])]
    print("length", length)
    print("direction", direction)
    (delta_row, delta_col) = DIRECTIONS[direction]
    (row, col) = loc
    loc = (row + delta_row * length, col + delta_col * length)
    print("->loc", loc)
    for _ in range(length):
        path.append(direction)

print("Final location:", loc)
print("Path length:", len(path))
print("Total area:", total_area(path))


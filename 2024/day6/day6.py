from sys import stdin

Directions = {
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
    "<": (-1, 0),
}

Rotations = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^",
}

class Map:
    def __init__(self):
        self.grid = []
        for line in stdin:
            self.grid.append([ch for ch in line.strip()])
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def at(self, x, y):
        if self.valid(x, y):
            return self.grid[y][x]
        else:
            return None

    def set(self, x, y, value):
        self.grid[y][x] = value

    def print(self):
        for y in range(self.height):
            print("".join(self.grid[y]))

    def num_xs(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y) == "X":
                    count += 1
        return count

    def take_guard(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y) in "^v<>":
                    guard = [x, y, self.at(x, y)]
                    self.set(x, y, ".")
                    return guard
    
    def walk_guard(self, guard):
        self.set(guard[0], guard[1], "X")
        while True:
            (dx, dy) = Directions[guard[2]]
            (x, y) = (guard[0] + dx, guard[1] + dy)
            if self.valid(x, y):
                if self.at(x, y) == "#":
                    guard[2] = Rotations[guard[2]]
                else:
                    guard[0], guard[1] = x, y
                    self.set(x, y, "X")
            else:
                return "Left"

map = Map()
guard = map.take_guard()
print(map.walk_guard(guard))
map.print()
print(map.num_xs())

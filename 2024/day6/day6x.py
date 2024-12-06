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
    def __init__(self, input):
        self.grid = []
        for line in input.split("\n"):
            self.grid.append([ch for ch in line.strip()])
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def copy(self):
        new_map = Map(self.display())
        return new_map

    def display(self):
        return "\n".join(["".join([ch for ch in line]) for line in self.grid])

    def valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def at(self, x, y):
        if self.valid(x, y):
            return self.grid[y][x]
        else:
            return None

    def set(self, x, y, value):
        self.grid[y][x] = value

    def num_xs(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y) == "X":
                    count += 1
        return count

    # Remove and return the guard from this map
    def take_guard(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.at(x, y) in "^v<>":
                    guard = [x, y, self.at(x, y)]
                    self.set(x, y, ".")
                    return guard
    
    # Simulate the guard walking, until they either "Leave" or "Loop".
    def walk_guard(self, guard):
        guard = [a for a in guard]
        positions = {(guard[0], guard[1], guard[2]),}
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
                    if (guard[0], guard[1], guard[2]) in positions:
                        return "Loop"
                    else:
                        positions.add((guard[0], guard[1], guard[2]))
            else:
                return "Leave"

    # Yield the locations of all places you might try to put an obstacle to distract the guard.
    def potential_obstacles(self, guard):
        map_copy = self.copy()
        map_copy.walk_guard(guard)
        for y in range(self.height):
            for x in range(self.width):
                if map_copy.at(x, y) == "X" and (x, y) != (guard[0], guard[1]):
                    yield (x, y)

# Read the map from stdin
map = Map("\n".join([line.strip() for line in stdin]))
guard = map.take_guard()

# Count the number of ways an obstacle can be placed to cause the guard to loop.
possibilities = 0
for (x, y) in map.potential_obstacles(guard):
    map_copy = map.copy()
    map_copy.set(x, y, "#")
    if map_copy.walk_guard(guard) == "Loop":
        print(x, y, "?", "yes")
        possibilities += 1
    else:
        print(x, y, "?", "no")

print(map.display())
print(possibilities)

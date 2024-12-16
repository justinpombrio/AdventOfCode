from sys import stdin

DIRECTIONS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

ROTATIONS = {
    "N": ["E", "W"],
    "S": ["E", "W"],
    "E": ["N", "S"],
    "W": ["N", "S"],
}

class Grid:
    def __init__(self):
        self.cells = []
        for line in stdin:
            self.add_row(line.strip())

    def add_row(self, line):
        row = []
        for ch in line:
            if ch in "#.":
                row.append(ch)
            elif ch == "S":
                self.start = (len(row), len(self.cells))
                row.append(".")
            elif ch == "E":
                self.end = (len(row), len(self.cells))
                row.append(".")
            else:
                raise Exception("Bad input char", ch)
        self.cells.append(row)

    def display(self):
        return "\n".join(["".join([ch for ch in line]) for line in self.cells])

    def get(self, x, y):
        return self.cells[y][x]

    def next(self, x, y, direction, cost, path):
        dx, dy = DIRECTIONS[direction]
        if self.get(x + dx, y + dy) == ".":
            yield (x + dx, y + dy, direction, cost + 1, path + [(x + dx, y + dy)])
        for rotation in ROTATIONS[direction]:
            yield (x, y, rotation, cost + 1000, path)

    def search(self):
        frontier = [(self.start[0], self.start[1], "E", 0, [self.start])]
        explored = set()
        ideal_cost = 1e10
        while frontier:
            cheapest, cheapest_index = 1e10, None
            for i in range(len(frontier)):
                cost = frontier[i][3]
                if cost < cheapest:
                    cheapest, cheapest_index = cost, i
            (x, y, direction, cost, path) = frontier[cheapest_index]
            print("Frontier size:", len(frontier))
            print("  Cost:", cost)
            print("  Path len:", len(path))
            del frontier[cheapest_index]
            if (x, y) == self.end:
                ideal_cost = cost
                yield (cost, path)
            if cost > ideal_cost:
                return
            explored.add((x, y, direction))
            for option in self.next(x, y, direction, cost, path):
                x, y, direction, cost, path = option
                if (x, y, direction) not in explored and option not in frontier:
                    frontier.append(option)

grid = Grid()
print(grid.display())
good_seats = set()
for (cost, path) in grid.search():
    print("Found a best path:")
    print("  Cost:", cost)
    print("  Path len:", len(path))
    for (x, y) in path:
        good_seats.add((x, y))
print("Best Cost:", cost)
print("Number of good seats:", len(good_seats))

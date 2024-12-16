from sys import stdin

MOTIONS = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}

class Grid:
    def __init__(self):
        self.cells = []

    def add_row(self, line):
        row = []
        for ch in line:
            if ch == "#":
                row.append("#")
                row.append("#")
            elif ch == "O":
                row.append("[")
                row.append("]")
            elif ch == ".":
                row.append(".")
                row.append(".")
            elif ch == "@":
                self.robot = (len(row), len(self.cells))
                row.append("@")
                row.append(".")
            else:
                raise Exception("Bad input char", ch)
        self.cells.append(row)

    def display(self):
        return "\n".join(["".join([ch for ch in line]) for line in self.cells])

    def coords(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells[0])):
                yield (x, y)

    def get(self, x, y):
        return self.cells[y][x]

    def set(self, x, y, ch):
        self.cells[y][x] = ch

    def gps(self):
        total = 0
        for (x, y) in self.coords():
            if self.get(x, y) == "[":
                total += 100 * y + x
        return total

    def move_one(self, source, x, y, dx, dy, commit):
        assert self.get(x, y) == source
        obstacle = self.get(x + dx, y + dy)
        if obstacle == ".":
            if commit:
                self.set(x + dx, y + dy, source)
                self.set(x, y, ".")
            return True
        elif obstacle == "#":
            assert not commit
            allowed = False
        else:
            assert obstacle in "[]"
            if dx == -1 and obstacle == "[":
                assert not commit
                return True
            if dx == 1 and obstacle == "]":
                assert not commit
                return True
            allowed = self.move(obstacle, x + dx, y + dy, dx, dy, commit)
            if commit:
                self.set(x + dx, y + dy, source)
                self.set(x, y, ".")
            return allowed

    def move(self, source, x, y, dx, dy, commit):
        if source == "[":
            return (self.move_one("]", x+1, y, dx, dy, commit)
                and self.move_one("[", x, y, dx, dy, commit))
        elif source == "]":
            return (self.move_one("[", x-1, y, dx, dy, commit)
                and self.move_one("]", x, y, dx, dy, commit))
        else:
            assert source == "@"
            return self.move_one("@", x, y, dx, dy, commit)

    def move_robot(self, motion):
        (x, y) = self.robot
        (dx, dy) = motion
        if self.move("@", x, y, dx, dy, False):
            self.move("@", x, y, dx, dy, True)
            self.robot = (x + dx, y + dy)

def read_grid_and_motions():
    reading_motions = False
    grid = Grid()
    motions = []
    for line in stdin:
        line = line.strip()
        if line == "":
            reading_motions = True
        if reading_motions:
            for ch in line:
                motions.append(MOTIONS[ch])
        else:
            grid.add_row(line)
    return (grid, motions)

(grid, motions) = read_grid_and_motions()

print(grid.display())
for motion in motions:
    print(motion)
    grid.move_robot(motion)
    print(grid.display())
print("GPS", grid.gps())

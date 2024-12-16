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
        self.cells.append([ch for ch in line.strip()])

    def finish(self):
        for (x, y) in self.coords():
            if self.get(x, y) == "@":
                self.robot = (x, y)
                return

    def display(self):
        return "\n".join([" ".join([ch for ch in line]) for line in self.cells])

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
            if self.get(x, y) == "O":
                total += 100 * y + x
        return total

    def move_robot(self, motion):
        (x, y) = self.robot
        (dx, dy) = motion
        (x2, y2) = (x + dx, y + dy)
        while self.get(x2, y2) == "O":
            (x2, y2) = (x2 + dx, y2 + dy)
        obstacle = self.get(x2, y2)
        if obstacle == ".":
            # All the rocks shift one, the robot moves one
            self.set(x2, y2, "O")
            self.robot = (x + dx, y + dy)
            self.set(x + dx, y + dy, "@")
            self.set(x, y, ".")
        elif obstacle == "#":
            # Pushing against a wall, nothing can move
            return
        else:
            raise Exception("Bad obstacle", obstacle)

def read_grid_and_motions():
    reading_motions = False
    grid = Grid()
    motions = []
    for line in stdin:
        line = line.strip()
        if line == "":
            grid.finish()
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

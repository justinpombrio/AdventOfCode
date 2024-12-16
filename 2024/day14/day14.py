from sys import stdin
import re

PART_2 = True

REGEX_SIZE = re.compile("width=([0-9]*) height=([0-9]*)")
REGEX_ROBOT = re.compile("p=([0-9]*),([0-9]*) v=(-?[0-9]*),(-?[0-9]*)")

STEPS = 100

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [["." for _ in range(width)] for _ in range(height)]

    def display(self):
        return "\n".join(["".join([str(cell) for cell in row]) for row in self.cells])

    def coords(self):
        for i in range(self.height):
            for j in range(self.width):
                yield (i, j)

    def get(self, i, j):
        return self.cells[i][j]

    def set(self, i, j, cell):
        self.cells[i][j] = cell
    
    def clear(self):
        for i, j in self.coords():
            self.set(i, j, ".")

    def place_robot(self, robot):
        i, j = robot.y, robot.x
        if self.get(i, j) == ".":
            self.set(i, j, 1)
        else:
            self.set(i, j, self.get(i, j) + 1)

    def quadrant_counts(self):
        counts = [0, 0, 0, 0]
        for i, j in self.coords():
            ch = self.get(i, j)
            n = 0 if ch == "." else ch
            if i < self.height // 2:
                if j < self.width // 2:
                    counts[0] += n
                elif j > self.width // 2:
                    counts[1] += n
            elif i > self.height // 2:
                if j < self.width // 2:
                    counts[2] += n
                elif j > self.width // 2:
                    counts[3] += n
        return counts

    def safety_factor(self):
        a, b, c, d = self.quadrant_counts()
        return a * b * c * d

class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.x = px
        self.y = py

    def display(self):
        return "Robot: " + str((self.px, self.py, self.vx, self.vy))

    def move(self, steps):
        self.x = (self.px + steps * self.vx) % width
        self.y = (self.py + steps * self.vy) % height

robots = []
for line in stdin:
    line = line.strip()
    match_size = REGEX_SIZE.match(line)
    match_robot = REGEX_ROBOT.match(line)
    if match_size is not None:
        width, height = int(match_size.group(1)), int(match_size.group(2))
        grid = Grid(width, height)
    elif match_robot is not None:
        x, y = int(match_robot.group(1)), int(match_robot.group(2))
        vx, vy = int(match_robot.group(3)), int(match_robot.group(4))
        robots.append(Robot(x, y, vx, vy))
    else:
        raise Exception("Bad line", line)

print("Size", width, height)
for robot in robots:
    grid.place_robot(robot)
print(grid.display())

print()
grid.clear()
for robot in robots:
    robot.move(STEPS)
    grid.place_robot(robot)
print(grid.display())
print()
print("Steps", STEPS)
print("Safety factor", grid.safety_factor())

if PART_2:
    for steps in range(100000):
        grid.clear()
        for robot in robots:
            robot.move(steps)
            grid.place_robot(robot)
        safety = grid.safety_factor()
        if steps % 1000 == 0:
            print("  Steps:", steps, "Safety factor:", safety)
        if safety < 100000000:
            print(grid.display())
            print("  Safety factor:", safety)
            print("  Steps:", steps)

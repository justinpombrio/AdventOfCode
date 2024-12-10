from sys import stdin

NEIGHBORS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]

class Grid:
    def __init__(self, text):
        self.grid = []
        for line in text.split("\n"):
            self.grid.append(["." if ch == "." else int(ch) for ch in line])
    
    def display(self):
        return "\n".join(["".join([str(ch) for ch in line]) for line in self.grid])

    def valid(self, y, x):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def at(self, y, x):
        return self.grid[y][x]

    def positions(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                yield (y, x)

    def trailheads(self):
        for (y, x) in self.positions():
            if self.at(y, x) == 0:
                yield (y, x)

    def neighbors(self, y, x):
        for (dy, dx) in NEIGHBORS:
            y2, x2 = y + dy, x + dx
            if self.valid(y2, x2):
                yield (y2, x2)

    def score_trailhead(self, y, x):
        frontier = {(y, x),}
        height = 0
        while height < 9:
            height += 1
            new_frontier = set()
            for (y, x) in frontier:
                for (y2, x2) in self.neighbors(y, x):
                    if self.at(y2, x2) != height:
                        new_frontier.add((y2, x2))
            frontier = new_frontier
        return len(frontier)
    
    def score(self):
        return sum([self.score_trailhead(y, x) for (y, x) in self.trailheads()])

    def rate_trailhead(self, y, x):
        frontier = {(y, x): 1}
        height = 0
        while height < 9:
            height += 1
            new_frontier = {}
            for (y, x) in frontier:
                for (y2, x2) in self.neighbors(y, x):
                    if self.at(y2, x2) == height:
                        if (y2, x2) not in new_frontier:
                            new_frontier[(y2, x2)] = 0
                        new_frontier[(y2, x2)] += frontier[(y, x)]
            frontier = new_frontier
        return sum([frontier[key] for key in frontier])

    def rating(self):
        return sum([self.rate_trailhead(y, x) for (y, x) in self.trailheads()])

grid = Grid("\n".join([line.strip() for line in stdin]))
print(grid.display())
print("Trailheads:", list(grid.trailheads()))
print("Score:", grid.score())
print("Rating:", grid.rating())

from sys import stdin

PART_2 = True

NEIGHBORS = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1)
]

class Garden:
    def __init__(self, text):
        self.grid = [[(ch, None) for ch in line] for line in text.split("\n")]

        print(self.display())
        print()

        self.regions = []
        self.total_cost = 0
        next_region_id = 0
        for (i, j) in self.cells():
            if self.get(i, j)[1] is None:
                ch, area, perim = self.flood_region(i, j, next_region_id)
                self.regions.append((ch, area, perim))
                print("region", ch, area, "*", perim, "=", area * perim)
                self.total_cost += area * perim
                next_region_id += 1

        print()
        print("total cost:", self.total_cost)

    def display(self):
        return "\n".join(["".join([ch for (ch, _) in line]) for line in self.grid])

    def display_regions(self):
        return "\n".join(["".join([str(r) for (_, r) in line]) for line in self.grid])

    def valid(self, i, j):
        return 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0])

    def get(self, i, j):
        return self.grid[i][j]

    def belongs_to_region(self, i, j, region_id):
        return self.valid(i, j) and self.get(i, j)[1] == region_id

    def get_region(self, i, j):
        if self.valid(i, j):
            return self.get(i, j)[1]
        else:
            return None

    def set_region(self, i, j, region):
        (ch, _) = self.grid[i][j]
        self.grid[i][j] = (ch, region)

    def cells(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                yield (i, j)

    def neighbors(self, i, j):
        for (di, dj) in NEIGHBORS:
            yield (i + di, j + dj)

    def valid_neighbors(self, i, j):
        for (i2, j2) in self.neighbors(i, j):
            if self.valid(i2, j2):
                yield (i2, j2)

    def flood_region(self, i, j, region_id):
        (ch, _) = self.get(i, j)
        area = 0
        perimeter = 0
        frontier = [(i, j)]
        while frontier:
            (i, j) = frontier.pop()
            if self.valid(i, j) and self.get(i, j) == (ch, None):
                self.set_region(i, j, region_id)
                area += 1
                for (i2, j2) in self.neighbors(i, j):
                    frontier.append((i2, j2))
            elif not self.valid(i, j) or self.get(i, j)[0] != ch:
                perimeter += 1
        if PART_2: perimeter = self.discount_perimeter(region_id)
        return ch, area, perimeter

    def discount_perimeter(self, region_id):
        perim = 0

        for i in range(len(self.grid) + 1):
            x1, y1 = (False, False)
            for j in range(len(self.grid[0])):
                x2 = self.belongs_to_region(i - 1, j, region_id)
                y2 = self.belongs_to_region(i, j, region_id)
                if (x1, y1) != (x2, y2) and ((x2 and not y2) or (y2 and not x2)):
                    perim += 1
                x1, y1 = x2, y2

        for j in range(len(self.grid[0]) + 1):
            x1, y1 = (False, False)
            for i in range(len(self.grid) + 1):
                x2 = self.belongs_to_region(i, j - 1, region_id)
                y2 = self.belongs_to_region(i, j, region_id)
                if (x1, y1) != (x2, y2) and ((x2 and not y2) or (y2 and not x2)):
                    perim += 1
                x1, y1 = x2, y2

        return perim

garden = Garden(stdin.read().strip())

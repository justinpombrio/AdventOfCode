import sys

class BrickSet:
    def __init__(self):
        self.bricks = set()
        self.occupied = set()

    def add_brick(self, brick):
        if all([cube not in self.occupied for cube in brick_cubes(brick)]):
            for cube in brick_cubes(brick):
                self.occupied.add(cube)
            self.bricks.add(brick)
            return True
        else:
            return False

    def remove_brick(self, brick):
        self.bricks.remove(brick) # error if not present
        for cube in brick_cubes(brick):
            self.occupied.remove(cube)

    def lower_brick(self, brick):
        self.remove_brick(brick)
        lowered_brick = lower(brick)
        if lowered_brick is not None and self.add_brick(lowered_brick):
            return True
        else:
            assert self.add_brick(brick) # put it back
            return False

    def lower_all_bricks(self):
        falling = set()
        done = False
        while not done:
            done = True
            for brick in list(self.bricks):
                if self.lower_brick(brick):
                    falling.add(brick[0])
                    done = False
        return falling

    def copy(self):
        copied = BrickSet()
        for brick in self.bricks:
            copied.add_brick(brick)
        return copied

    def brick_is_safe(self, brick):
        brickset = self.copy()
        brickset.remove_brick(brick)
        return not brickset.lower_all_bricks()

    def count_safe_bricks(self):
        count = 0
        for brick in list(self.bricks):
            if self.brick_is_safe(brick):
                count += 1
        return count

    def count_falling_bricks(self):
        count = 0
        for n, brick in enumerate(list(self.bricks)):
            brickset = self.copy()
            brickset.remove_brick(brick)
            falling = len(brickset.lower_all_bricks())
            print("brick:", n, "/", len(self.bricks), "falling:", falling, "total:", count)
            count += falling
        return count

    def display(self):
        print(self.bricks)

def brick_cubes(brick):
    i, start, end = brick
    x1, y1, z1 = start
    x2, y2, z2 = end
    if x1 != x2:
        for x in range(x1, x2 + 1):
            yield (x, y1, z1)
    elif y1 != y2:
        for y in range(y1, y2 + 1):
            yield (x1, y, z1)
    elif z1 != z2:
        for z in range(z1, z2 + 1):
            yield (x1, y1, z)
    else:
        yield (x1, y1, z1)

def lower(brick):
    i, start, end = brick
    x1, y1, z1 = start
    x2, y2, z2 = end
    if z1 == 0 or z2 == 0:
        return None # at ground
    return (i, (x1, y1, z1 - 1), (x2, y2, z2 - 1))

bricks = BrickSet()
for i, line in enumerate(open(sys.argv[1], 'r')):
    line = line.strip()
    fst, snd = line.split("~")
    x, y, z = fst.split(",")
    start = int(x), int(y), int(z)
    x, y, z = snd.split(",")
    end = int(x), int(y), int(z)
    bricks.add_brick((i, start, end))

bricks.display()
bricks.lower_all_bricks()
print("lowered")
bricks.display()
print("TOTAL:", bricks.count_falling_bricks())

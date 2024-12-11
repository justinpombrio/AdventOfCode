import sys

class Stones:
    def __init__(self):
        self.stones = {}

    def insert(self, count, stone):
        if stone not in self.stones:
            self.stones[stone] = 0
        self.stones[stone] += count

    def display(self):
        return " ".join([str(self.stones[stone]) + "*" + stone for stone in self.stones])

    def count(self):
        return sum([self.stones[stone] for stone in self.stones])
    
    def blink(self):
        new_stones = Stones()
        for stone in self.stones:
            count = self.stones[stone]
            if stone == "0":
                new_stones.insert(count, "1")
            elif len(stone) % 2 == 0:
                new_stones.insert(count, stone[:len(stone)//2])
                new_stones.insert(count, str(int(stone[len(stone)//2:])))
            else:
                new_stones.insert(count, str(2024 * int(stone)))
        self.stones = new_stones.stones

if len(sys.argv) != 2:
    raise Exception("Usage: pass the number of iterations")

iterations = int(sys.argv[1])

stones = Stones()
for stone in sys.stdin.read().strip().split(" "):
    stones.insert(1, stone)

print(stones.display())
for i in range(iterations):
    stones.blink()
    print(stones.display())
    print("step", i+1)
    print("count", stones.count())

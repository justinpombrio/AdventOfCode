import sys

digit_names = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}

class Number:
    def __init__(self, row, col, digit):
        self.row = row
        self.col = col
        self.len = 1
        self.value = digit_names[digit]

    def next_pos(self):
        return (self.row, self.col + self.len)

    def add_digit(self, digit):
        self.len += 1
        self.value *= 10
        self.value += digit_names[digit]

    def is_adjacent_to(self, row, col):
        """Is (row, col) adjacent (incl diagonally) to this number?
        Also return True if (row, col) is colocated with this number,
        though that shouldn't matter."""
        return (row >= self.row - 1 and row <= self.row + 1
            and col >= self.col - 1 and col <= self.col + self.len)

# Find all symbols and numbers in the grid.
# Each symbol is stored as (row, col, symbol)
# Each number is stored as a Number
symbols = []
numbers = []
for (row, line) in enumerate(open(sys.argv[1], 'r')):
    line = line.strip()
    for (col, ch) in enumerate(line):
        if ch in digit_names:
            # See if we're extending an existing number
            for number in numbers:
                if number.next_pos() == (row, col):
                    number.add_digit(ch)
                    break
            # Otherwise, make a new number
            else:
                numbers.append(Number(row, col, ch))
        elif ch != ".":
            print("Symbol:", ch, "at", str(row) + "," + str(col))
            symbols.append((row, col, ch))

# Find and sum all "gears"
sum = 0
for (row, col, symbol) in symbols:
    if symbol == "*":
        adjacent_parts = list(filter(lambda n: n.is_adjacent_to(row, col), numbers))
        if len(adjacent_parts) == 2:
            part1 = adjacent_parts[0].value
            part2 = adjacent_parts[1].value
            # This _really_ isn't what 'ratio' means, but whatever
            ratio = part1 * part2 
            print("Gear:", part1, "*", part2, "=", ratio, "at", str(row) + "," + str(col))
            sum += ratio

print("\nSUM:")
print(sum)

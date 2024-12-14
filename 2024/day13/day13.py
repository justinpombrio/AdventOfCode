import re
from sys import stdin

PART_2 = True

REGEX_A = re.compile("Button A: X\\+([0-9]*), Y\\+([0-9]*)")
REGEX_B = re.compile("Button B: X\\+([0-9]*), Y\\+([0-9]*)")
REGEX_PRIZE = re.compile("Prize: X=([0-9]*), Y=([0-9]*)")

class ClawMachine:
    def __init__(self, button_a, button_b, prize):
        self.ax, self.ay = button_a
        self.bx, self.by = button_b
        self.px, self.py = prize
        self.button_a = button_a
        self.button_b = button_b
        self.prize = prize

    def solve(self):
        a = self.solve_a()
        b = self.solve_b()
        if a is None or b is None:
            return None
        else:
            return (a, b)

    def solve_a(self):
        ax, ay = self.button_a
        bx, by = self.button_b
        px, py = self.prize

        numer = by * px - bx * py
        denom = ax * by - ay * bx
        if numer % denom == 0:
            return numer // denom
        else:
            return None

    def solve_b(self):
        ax, ay = self.button_a
        bx, by = self.button_b
        px, py = self.prize

        numer = ay * px - ax * py
        denom = bx * ay - ax * by
        if numer % denom == 0:
            return numer // denom
        else:
            return None

total_tokens = 0
for line in stdin:
    line = line.strip()
    match_a = REGEX_A.match(line)
    match_b = REGEX_B.match(line)
    match_prize = REGEX_PRIZE.match(line)
    if match_a:
        button_a = (int(match_a.group(1)), int(match_a.group(2)))
    elif match_b:
        button_b = (int(match_b.group(1)), int(match_b.group(2)))
    elif match_prize:
        prize = (int(match_prize.group(1)), int(match_prize.group(2)))
        if PART_2:
            prize = (10000000000000 + prize[0], 10000000000000 + prize[1])
    elif line == "":
        print("A", button_a, "B", button_b, "Prize", prize)
        machine = ClawMachine(button_a, button_b, prize)
        solution = machine.solve()
        if solution:
            tokens = 3 * solution[0] + solution[1]
            print("  ", solution[0], solution[1], tokens)
            total_tokens += tokens
        else:
            print("  No solution")
    else:
        raise Exception("Bad line:", line)

print("Total tokens:", total_tokens)

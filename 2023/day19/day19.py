import sys

class RangeSet:
    def __init__(self, ranges):
        self.ranges = ranges

    def count(self):
        return sum([b - a for (a, b) in self.ranges])

    def union(self, a, b):
        before = [(x, y) for (x, y) in self.ranges if y < a]
        after = [(x, y) for (x, y) in self.ranges if x > b]
        middle = [(x, y) for (x, y) in self.ranges if not (y < a or x > b)]
        if len(middle) == 0:
            return RangeSet(before + [(a, b)] + after)
        else:
            (x, y) = (middle[0][0], middle[-1][1])
            return RangeSet(before + [(min(a, x), max(b, y))] + after)

    def union_all(self, rangeset):
        result = self.copy()
        for (a, b) in rangeset.ranges:
            result = result.union(a, b)
        return result

    def intersect(self, a, b):
        ranges = []
        for (x, y) in self.ranges:
            if y < a or x > b:
                continue
            ranges.append((max(x, a), min(y, b)))
        return RangeSet(ranges)

    def copy(self):
        return RangeSet([(min, max) for (min, max) in self.ranges])

class PartSet:
    def __init__(self, attrs):
        self.attrs = attrs

    def count(self):
        total = 1
        for attr in "xmas":
            total *= self.attrs[attr].count()
        return total

    def union(self, other):
        attrs = {}
        for attr in "xmas":
            attrs[attr] = self.attrs[attr].copy().union_all(other.attrs[attr])
        return PartSet(attrs)

    def condition(self, attr, op, num):
        if op == ">":
            a, b, c, d = num + 1, 4001, 1, num + 1
        elif op == "<":
            a, b, c, d = 1, num, num, 4001
        else:
            raise "bad"
        yes_set = self.copy()
        no_set = self.copy()
        yes_set.attrs[attr] = yes_set.attrs[attr].intersect(a, b)
        no_set.attrs[attr] = no_set.attrs[attr].intersect(c, d)
        return yes_set, no_set

    def copy(self):
        return PartSet({
            attr: rangeset.copy()
            for attr, rangeset in self.attrs.items()
        })

    def display(self):
        print("PartSet:")
        for attr in "xmas":
            print(" ", attr, "=")
            for (x, y) in self.attrs[attr].ranges:
                print("   ", x, "-", y)

def parse_step(step):
    if ":" in step:
        condition, consq = step.split(":")
        if ">" in condition:
            attr, num = condition.split(">")
            comparison = ">"
        elif "<" in condition:
            attr, num = condition.split("<")
            comparison = "<"
        else:
            raise "bad"
        return (comparison, (attr, int(num), consq))
    elif step == "A":
        return ("A", None)
    elif step == "R":
        return ("R", None)
    else:
        return ("goto", step)

total = 0
def acceptance2(rules, partset, steps):
    global total
    step = steps.pop(0)
    print("steps", step, steps)
    (op, args) = step
    if op in "<>":
        (attr, num, consq) = args
        partset_yes, partset_no = partset.condition(attr, op, num)
        acceptance2(rules, partset_no, steps)
        if consq == "A":
            total += partset_yes.count()
        elif consq == "R":
            pass
        else:
            acceptance2(rules, partset_yes, rules[consq])
    elif op == "A":
        total += partset.count()
    elif op == "R":
        pass
    elif op == "goto":
        acceptance2(rules, partset, rules[args])
    else:
        raise "bad"

rules = {}
for line in open(sys.argv[1], 'r'):
    line = line.strip()
    if line == "":
        partset = PartSet({ letter: RangeSet([(1, 4001)]) for letter in "xmas" })
        acceptance2(rules, partset, rules["in"])
        print("Number accepted:", total)
        #accepted.display()
        break
    rule_name, steps = line.split("{")
    steps = list(map(parse_step, steps[:-1].split(",")))
    rules[rule_name] = steps
    print(rule_name, "->", steps)

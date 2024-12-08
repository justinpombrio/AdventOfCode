from sys import stdin

PART_2 = True

# Check operations in reverse order
def check(expected, args):
    if len(args) == 1:
        if expected == args[0]:
            return True
    else:
        last = args[-1]
        # Could the last operation be a concat (||)? Part 2 only.
        if PART_2 and expected > last and str(expected).endswith(str(last)):
            # a = stuff || b  implies  a with the b suffix removed = stuff
            if check(int(str(expected)[:-len(str(last))]), args[:-1]):
                return True
        # Could the last operation be a multiplication?
        if expected >= last and expected % last == 0:
            # a = stuff * b  implies  a/b = stuff
            if check(expected // last, args[:-1]):
                return True
        # Could the last operation be a addition?
        if expected >= last:
            # a = stuff + b  implies  a-b = stuff
            return check(expected - last, args[:-1])
    return False

calibration = 0
for line in stdin:
    parts = line.strip().split(": ")
    expected = int(parts[0])
    args = list(map(int, parts[1].split(" ")))
    possible = check(expected, args)
    print(" ", expected, ":", args, "->", possible)
    if possible:
        calibration += expected

print("calibration", calibration)

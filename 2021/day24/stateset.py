import random

# NOTES:
# digits 4, 5, 8, 9 are typically 9

def get_register(regs, var):
    (w, x, y, z) = regs
    if var == "w": return w
    elif var == "x": return x
    elif var == "y": return y
    elif var == "z": return z
    else: raise "oops"

def set_register(regs, var, val):
    (w, x, y, z) = regs
    if var == "w": return (val, x, y, z)
    elif var == "x": return (w, val, y, z)
    elif var == "y": return (w, x, val, z)
    elif var == "z": return (w, x, y, val)
    else: raise "oops"

# 01234567890123
# 53998426997919 -> 0
#KNOWN = "59998426997979"
#KNOWN = "19998426997975" # too high
#KNOWN = "11998426997919" -> 9
#KNOWN = "19998426997975" # too high
#KNOWN = "13998426997915" -> 0
#KNOWN = "13998426991315" -> too high
#        "13621126997915" -> too high
#         13621126991315  -> too high
#         13621111481315
EXPECTED = 13621126991315
KNOWN = "13621126991315"
KNOWN = "1???1111??????"

def execute(regs, model, instr):
    op = instr[0]
    dest = instr[1]
    a = get_register(regs, dest)
    if len(instr) == 3:
        if instr[2] in "wxyz":
            b = get_register(regs, instr[2])
        else:
            b = int(instr[2])

    if op == "inp":
        if KNOWN[len(model)] != "?":
            possibilities = [int(KNOWN[len(model)])]
        else:
            possibilities = range(1, 10)
        return {set_register(regs, dest, n): model + [n]
                for n in possibilities}
    if op == "mul": result = a * b
    elif op == "add": result = a + b
    elif op == "mod": result = a % b
    elif op == "div" and a >= 0: result = a // b
    elif op == "div" and a < 0: result = (a + 1) // b
    elif op == "eql" and a == b: result = 1
    elif op == "eql" and a != b: result = 0
    else: raise "NYI"

    return {set_register(regs, dest, result): model}

def tonum(digits):
    n = 0
    for digit in digits:
        n *= 10
        n += digit
    return n

stateset = {(0, 0, 0, 0): []}
for (i, line) in enumerate(open("input.txt", "r")):
    instr = line.strip().split()

    new_stateset = {}
    for old_regs in stateset:
        old_model = stateset[old_regs]
        next_stateset = execute(old_regs, old_model, instr)
        for regs in next_stateset:
            model = next_stateset[regs]
            if regs in new_stateset:
                if tonum(model) < tonum(new_stateset[regs]):
                    new_stateset[regs] = model
            else:
                new_stateset[regs] = model
    stateset = new_stateset

    print ""
    print "Step", i, ":", line.strip()
    print "  Set size:", len(stateset)
    print "  Samples:"
#    for regs in stateset:
#        model = stateset[regs]
#        print "   ", regs, ":", model
    for _ in range(3):
        regs = random.choice(stateset.keys())
        model = stateset[regs]
        print "   ", regs, ":", tonum(model)

best = (1000000000, None)
for regs in stateset:
    (w, x, y, z) = regs
    model = stateset[regs]
    (least_z, best_model) = best
    if z < least_z or z <= least_z and tonum(model) < tonum(best_model):
        best = (z, model)
    if z == 0:
        print "a solution", tonum(model)

(z, model) = best
print "best model:", tonum(model), "z:", z
if tonum(model) != int(EXPECTED) and z == 0:
    print "woah!"

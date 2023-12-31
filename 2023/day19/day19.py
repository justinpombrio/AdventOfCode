import sys

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

def solve(rules, parts, steps):
    (op, args) = steps.pop(0)
    print("steps", op, args, steps)
    if op in "<>":
        (attr, num, consq) = args
        if consq == "A":
            return limit(parts, attr, op, num) + solve(rules, no(parts

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
        total = solve(rules, { attr: (1, 4001) for attr in "xmas" }, rules["in"])
        print("Number accepted:", total)
        break
    rule_name, steps = line.split("{")
    steps = list(map(parse_step, steps[:-1].split(",")))
    rules[rule_name] = steps
    print(rule_name, "->", steps)

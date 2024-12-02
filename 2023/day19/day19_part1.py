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

def follow_rules(rules, part):
    rule = rules["in"]
    while True:
        print("rule", rule)
        for (op, args) in rule:
            if op in "<>":
                (attr, num, consq) = args
                if op == ">" and part[attr] > num or op == "<" and part[attr] < num:
                    if consq in "AR":
                        return consq
                    else:
                        rule = rules[consq]
                        break
            elif op in "AR":
                return op
            elif op == "goto":
                rule = rules[args]
                break

rules = {}
on_parts = False
total = 0
for line in open(sys.argv[1], 'r'):
    line = line.strip()
    if not on_parts:
        if line == "":
            on_parts = True
            continue
        rule_name, steps = line.split("{")
        steps = list(map(parse_step, steps[:-1].split(",")))
        rules[rule_name] = steps
        print(rule_name, "->", steps)
    else:
        part = {}
        for attrs in line[1:-1].split(","):
            attr, value = attrs.split("=")
            part[attr] = int(value)
        if follow_rules(rules, part) == "A":
            total += part["x"] + part["m"] + part["a"] + part["s"]

print("Total:", total)

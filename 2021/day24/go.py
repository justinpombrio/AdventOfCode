# STATE: (w, x, y, z)

def get(state, var):
    i = "wxyz".index(var)
    assert 0 <= i <= 4
    return state[i]

def set(state, var, val):
    i = "wxyz".index(var)
    assert 0 <= i <= 4
    state[i] = val

def value(state, arg):
    if isinstance(arg, str):
        return get(state, arg)
    elif isinstance(arg, int):
        return arg
    else:
        raise "oops"

def divide(a, b):
    if a >= 0:
        return a // b
    else:
        return a // b
        #return (a + 1) // b
assert divide(3, 2) == 1
assert divide(2, 2) == 1
#assert divide(-3, 2) == -1
assert divide(-2, 2) == -1

def modulo(a, b):
    assert a >= 0
    assert b > 0
    return a % b
assert modulo(2, 2) == 0
assert modulo(3, 2) == 1

def equal(a, b):
    if a == b:
        return 1
    else:
        return 0
assert equal(1, 2) == 0
assert equal(2, 2) == 1

def execute(model, state, instr):
    op = instr[0]
    a = instr[1]
    if len(instr) == 3:
        b = instr[2]
    if op == "inp":
        set(state, a, model[0])
        model = model[1:]

    elif op == "add":
        set(state, a, get(state, a) + value(state, b))
    elif op == "mul":
        set(state, a, get(state, a) * value(state, b))
    elif op == "div":
        set(state, a, divide(get(state, a), value(state, b)))
    elif op == "mod":
        set(state, a, modulo(get(state, a), value(state, b)))
    elif op == "eql":
        set(state, a, equal(get(state, a), value(state, b)))
    return (model, state)

def run(model, instrs):
    state = [0, 0, 0, 0]
    for instr in instrs:
        (model, state) = execute(model, state, instr)
        #print "exec", instr, "->", state
    if get(state, "z") == 0:
        print "answer:", model
        raise Exception("done!")
    return get(state, "z")

instrs = []
for line in open("input.txt", "r"):
    parts = line.strip().split()
    if len(parts) == 3 and parts[2] not in "wxyz":
        parts[2] = int(parts[2])
    instrs.append(parts)

run(map(int, "13579246899999"), instrs)

def possibilities(model_template):
    models = [0]
    for digit in model_template:
        if digit == "*":
            models = [10 * m + d for m in models for d in range(1, 10)]
        else:
            models = [10 * m + int(digit) for m in models]
    return models

def tonum(digits):
    n = 0
    for digit in digits:
        n *= 10
        n += digit
    return n

model_template = "11998496977919"
correct_answer = "119984*6977919"
#                 11998426997919
# or             "--------5-----"

least = 1000000000
for model in possibilities(model_template):
    model = map(int, str(model))
    result = run(model, instrs)
    least = min(least, result)
    print tonum(model), "->", result
print "best:"
print tonum(model), "->", least


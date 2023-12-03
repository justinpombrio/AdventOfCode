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

def symbolic_add(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a + b
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return ["add", a, b]

def symbolic_mul(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a * b
    if a == 0:
        return 0
    elif b == 0:
        return 0
    elif a == 1:
        return b
    elif b == 1:
        return a
    else:
        return ["mul", a, b]

def symbolic_div(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return divide(a, b)
    if a == 0:
        return 0
    elif b == 1:
        return a
    return ["div", a, b]

def divide(a, b):
    if a >= 0:
        return a // b
    else:
        return (a + 1) // b
assert divide(3, 2) == 1
assert divide(2, 2) == 1
assert divide(-3, 2) == -1
assert divide(-2, 2) == -1

def symbolic_mod(a, b):
    if a == ['add', '$0', 8] and b == 26:
        return ['add', '$0', 8]
    if isinstance(a, int) and isinstance(b, int):
        return modulo(a, b)
    if a == 0:
        return 0
    elif b == 1:
        return 1
    elif a == b:
        return 0
    else:
        return ["mod", a, b]

def modulo(a, b):
    assert a >= 0
    assert b > 0
    return a % b
assert modulo(2, 2) == 0
assert modulo(3, 2) == 1

def symbolic_eql(a, b):
    if a == ['add', '$0', '8'] and b == 0:
        return 0
    if isinstance(a, int) and isinstance(b, int):
        return equal(a, b)
    if isinstance(a, str) and a.startswith("$") and isinstance(b, int):
        if b == 0:
            return 0
        if b > 9:
            return 0
    if isinstance(b, str) and b.startswith("$") and isinstance(a, int):
        if a == 0:
            return 0
        if a > 9:
            return 0
    if a == b:
        return 1
    else:
        return ["eql", a, b]

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

    if op == "inp":
        set(state, a, model[0])
        model = model[1:]
        return (model, state)

    b = instr[2]
    a_val = get(state, a)
    b_val = value(state, b)

    if op == "add": result = symbolic_add(a_val, b_val)
    elif op == "mul": result = symbolic_mul(a_val, b_val)
    elif op == "div": result = symbolic_div(a_val, b_val)
    elif op == "mod": result = symbolic_mod(a_val, b_val)
    elif op == "eql": result = symbolic_eql(a_val, b_val)
    set(state, a, result)

    return (model, state)

def symbolic_run(instrs):
    state = [0, 0, 0, 0]
    model = ["$" + str(i) for i in range(14)]
    for instr in instrs:
        (model, state) = execute(model, state, instr)
        print "exec", instr, "->", state
    print "result", get(state, "z")
    if get(state, "z") == 0:
        print "answer:", model
        raise Exception("done!")

def run(model, instrs):
    state = [0, 0, 0, 0]
    for instr in instrs:
        (model, state) = execute(model, state, instr)
        print "exec", instr, "->", state
    print "result", get(state, "z")
    if get(state, "z") == 0:
        print "answer:", model
        raise Exception("done!")

def count_down(model):
    model[13] -= 1
    for i in reversed(range(0, 14)):
        if model[i] == 0:
            model[i] = 9
            model[i-1] -= 1
        else:
            break
    return model

instrs = []
for line in open("input.txt", "r"):
    parts = line.strip().split()
    if len(parts) == 3 and parts[2] not in "wxyz":
        parts[2] = int(parts[2])
    instrs.append(parts)

symbolic_run(instrs)


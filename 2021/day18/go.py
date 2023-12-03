filename = "example.txt"

text = None

def take():
    global text
    ch = text[0]
    text = text[1:]
    return ch

def parse():
    ch = take()
    if ch == "[":
        l = parse()
        take() # comma
        r = parse()
        take() # ]
        return [l, r]
    else:
        return int(ch)

trees = []
for line in open(filename, "r"):
    text = line.strip()
    tree = parse()
    trees.append(tree)

def split(n):
    return [n // 2, (n + 1) // 2]

def magnitude(tree):
    if isinstance(tree, int):
        return tree
    else:
        return 3 * tree[0] + 2 * tree[1]

def normalize(tree, depth, addleft, addright):
    result = normalize_inner(tree, depth, addleft, addright)
    print "  normalize", tree, "d:", depth, "+:", addleft, addright, " = ", result
    if result[0] > 0 or result[2] > 0:
        print "explode!", result
    return result

def normalize_inner(tree, depth, addleft, addright):
    if isinstance(tree, int):
        tree = tree + addleft + addright
        if tree > 9:
            [l, r] = split(tree)
            if depth >= 3:
                return (l, 0, r)
            else:
                return (0, [l, r], 0)
        else:
            return (0, tree, 0)
    elif depth >= 4:
        return (addleft + tree[0], 0, tree[1] + addright)
    else:
        (ll, left, lr) = normalize(tree[0], depth + 1, addleft, 0)
        initl = (ll, left, lr)
        ll0 = ll
        (rl, right, rr) = normalize(tree[1], depth + 1, lr, addright)
        initr = (rl, right, rr)
        rr0 = rr
        (ll, left, lr) = normalize(left, depth + 1, 0, rl)
        (rl, right, rr) = normalize(right, depth + 1, lr, 0)
        if rl > 0:
            raise "not handled"
        return (ll0 + ll, [left, right], rr0 + rr)

def normal(tree):
    (_, t, _) = normalize(tree, 0, 0, 0)
    return t

s = trees[0]
for tree in trees[1:]:
    print "tree", tree
    s = normal([s, tree])
    print "sum", s
    print ""

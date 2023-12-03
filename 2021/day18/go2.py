filename = "input.txt"

# parse each tree into a list of [depth, number]
trees = []
for line in open(filename, "r"):
    tree = []
    depth = 0
    for ch in line.strip():
        if ch == "[": depth += 1
        elif ch == ",": continue
        elif ch == "]": depth -= 1
        else: tree.append([depth, int(ch)])
    trees.append(tree)

def add(tree1, tree2):
    return [[d+1, n] for [d, n] in tree1] + [[d+1, n] for [d, n] in tree2]

def step(tree):
    changed = False
    # explode
    for i in range(len(tree)):
        [depth, n] = tree[i]
        if depth >= 5:
            (l, r) = (n, tree[i+1][1])
            if i-1 >= 0:
                tree[i-1][1] += l
            if i+2 < len(tree):
                tree[i+2][1] += r
            tree = tree[:i] + [[depth-1, 0]] + tree[i+2:]
            changed = True
            break
    if changed: return (tree, changed)
    # split
    for i in range(len(tree)):
        [depth, n] = tree[i]
        if n > 9:
            tree = (tree[:i]
                    + [[depth+1, n // 2], [depth+1, (n + 1) // 2]]
                    + tree[i+1:])
            changed = True
            break
    return (tree, changed)

def normalize(tree):
    while True:
        (tree, changed) = step(tree)
        if not changed: break
    return tree

# list of (depth, num) -> tree of nested pairs
def convert(tree):
    return convert_rec(tree, 0)[0]

def convert_rec(tree, depth):
    [d, n] = tree[0]
    if d == depth:
        return n, tree[1:]
    else:
        l, t = convert_rec(tree, depth + 1)
        r, t = convert_rec(t, depth + 1)
        return [l, r], t

def magnitude(tree):
    if isinstance(tree, int):
        return tree
    else:
        return 3 * magnitude(tree[0]) + 2 * magnitude(tree[1])

# PART 1:
#s = trees[0]
#for tree in trees[1:]:
#    print ""
#    result = normalize(add(s, tree))
#    print convert(s)
#    print "+", convert(tree)
#    print "=", convert(result)
#    s = result
# print ""
# print "total sum", convert(s)
# print "magnitude", magnitude(convert(s))

# PART 2:
biggest = 0
for i in range(len(trees)):
    for j in range(len(trees)):
        if i == j: continue
        tree1, tree2 = trees[i], trees[j]
        m = magnitude(convert(normalize((add(tree1, tree2)))))
        if m > biggest: biggest = m
print "biggest sum", biggest

filename = "input.txt"

for line in open(filename, "r"):
    parts = line.strip().split(" ")
    xpart = parts[2][2:-1]
    ypart = parts[3][2:]
    xparts = xpart.split("..")
    x0, x1 = int(xparts[0]), int(xparts[1])
    yparts = ypart.split("..")
    y0, y1 = int(yparts[0]), int(yparts[1])

def slow(n):
    if n > 0: return n - 1
    elif n < 0: return n + 1
    else: return 0

def step(x, y, vx, vy):
    #print "step", x, y, vx, vy
    return (x + vx, y + vy, slow(vx), vy - 1)

def in_target(x, y):
    return x >= x0 and x <= x1 and y >= y0 and y <= y1

STEPS = 1000
MIN = -100
MAX = 100

succ = 0
def simulate(vx, vy):
    global succ
    init = (vx, vy)
    max_y = 0
    x, y = 0, 0
    for t in range(STEPS):
        if in_target(x, y):
            succ += 1
            print "hit", (x, y), "with", init, "at", t, max_y, "count", succ
            return ((x, y), init, t, max_y)
        (x, y, vx, vy) = step(x, y, vx, vy)
        max_y = max(y, max_y)
    return None

def search():
    for vy in range(-200, 200):
        for vx in range(0, 500):
            result = simulate(vx, vy)
            if result:
                continue

print "x", x0, "..", x1
print "y", y0, "..", y1
print ""

search()

for vx in range(0, 100):
    init = vx
    x = 0
    while vx > 0:
        x += vx
        vx = slow(vx)
    if x >= x0 and x <= x1:
        print "possible vx", init

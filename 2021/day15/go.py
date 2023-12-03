import sys

filename = "input.txt"

grid = []
for line in open(filename, "r"):
  grid.append([int(ch) for ch in line.strip()])


width = len(grid[0])
height = len(grid)

fullwidth = width * 5
fullheight = height * 5

def get(x, y):
  if x >= 0 and y >= 0 and x < fullwidth and y < fullheight:
    return wrap(grid[y % height][x % width] + (y / height) + (x / width))
  else:
    return None

def wrap(n):
  m = n % 9
  if m == 0: return 9
  else: return m

def neighbors(x, y):
  return filter(is_valid, [(x-1,y), (x+1,y), (x,y-1), (x,y+1)])

def is_valid((x, y)):
  return get(x, y) is not None

explored = {}
frontier = {(0, 0): 0}
while not len(frontier) == 0:
  positions = [(x, y, frontier[(x, y)]) for (x, y) in frontier]
  positions.sort(key = lambda (x, y, d): d)
  (x, y, d) = positions[0]
  del frontier[(x, y)]

  print "exploring", x, y, d
  print "explored", len(explored)
  print "frontier", len(frontier)

  for (x2, y2) in neighbors(x, y):
    if (x2, y2) not in explored:
      d2 = d + get(x2, y2)
      if (x2, y2) in frontier:
        frontier[(x2, y2)] = min(frontier[(x2, y2)], d2)
      else:
        frontier[(x2, y2)] = d2
  explored[(x, y)] = d

for y in range(fullheight):
  for x in range(fullwidth):
    d = get(x, y)
    sys.stdout.write(str(d))
  print ""

print grid
print explored
print "dist", explored[(fullwidth-1,fullheight-1)]
print "get", get(fullwidth-1, fullheight-1)

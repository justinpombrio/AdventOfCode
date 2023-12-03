filename = "input.txt"

grid = []
for line in open(filename, "r"):
  grid.append([int(d) for d in line.strip()])

width = len(grid[0])
height = len(grid)

def get(x, y): return grid[y][x]

def valid((x, y)):
  return 0 <= x <= width-1 and 0 <= y <= height-1

def neighbors(x, y):
  return filter(valid, [(x-1,y), (x+1,y), (x,y-1), (x,y+1)])

def is_low(x, y):
  low = True
  for (x2, y2) in neighbors(x, y):
    if get(x2, y2) <= get(x, y):
      low = False
  return low

def all_points():
  return [(x, y) for x in range(width) for y in range(height)]

#basins = [[(x, y)] for (x, y) in all_points() if get(x, y) != 9]

def flow(x, y):
  while not is_low(x, y):
    for (x2, y2) in neighbors(x, y):
      if get(x2, y2) < get(x, y):
        (x, y) = (x2, y2)
  return (x, y)

m = {}
for (x, y) in [(x, y) for (x, y) in all_points() if get(x, y) != 9]:
  lowest = flow(x, y)
  if lowest not in m: m[lowest] = []
  m[lowest].append((x, y))

print m

basins = []
for k in m:
  basins.append(m[k])

basins.sort(key=len)
basins.reverse()

print basins
for basin in basins:
  print len(basin)

print len(basins[0])*len(basins[1])*len(basins[2])

# def update_basins(old_basins):
#   new_basins = []
#   for basin in old_basins:
#     for (x, y) in basin:


# s = 0
# for (x, y) in all_points():
#   if is_low(x, y):
#     print (x, y), get(x,y)
#     s += get(x,y)+1
# print s

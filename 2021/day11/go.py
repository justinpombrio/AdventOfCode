filename = "input.txt"

grid = []
for line in open(filename, "r"):
  grid.append([int(ch) for ch in line.strip()])

def inc(n):
  if n == 10: return 10
  else: return n + 1

width = len(grid[0])
height = len(grid)

def is_valid((x, y)):
  return x >= 0 and y >= 0 and x < width and y < height

def neighbors(x, y):
  return filter(is_valid,
    [(x-1, y-1), (x-1, y), (x-1, y+1),
     (x, y-1), (x, y), (x, y+1),
     (x+1, y-1), (x+1, y), (x+1, y+1)])

def show(grid):
  for y in range(height):
    print grid[y]
  print ""

i = 0
def next(grid):
  global i
  i += 1
  for x in range(width):
    for y in range(height):
      grid[y][x] += 1
  flashes = 0
  while True:
    new_flashes = 0
    for x in range(width):
      for y in range(height):
        if grid[y][x] == 10:
          new_flashes += 1
          grid[y][x] = 0
          for (x2, y2) in neighbors(x, y):
            if grid[y2][x2] != 0 and grid[y2][x2] != 10:
              grid[y2][x2] += 1
    if new_flashes > 0:
      flashes += new_flashes
    else:
      break
  if flashes == width * height:
    print "!!!!", i
    raise ""
  return flashes

show(grid)
count = 0
for _ in range(1000000):
  count += next(grid)
  print i
  show(grid)
print ""
print count

import sys

filename = "input.txt"

lines = []
for fileline in open(filename, "r"):
  arrow = fileline.strip().split()
  left = arrow[0].split(",")
  right = arrow[2].split(",")
  lines.append(map(int, [left[0], left[1], right[0], right[1]]))
print len(lines), "lines"

biggest = 0
for line in lines:
  biggest = max(biggest, line[0])
  biggest = max(biggest, line[1])
  biggest = max(biggest, line[2])
  biggest = max(biggest, line[3])
biggest = biggest + 1
print "biggest", biggest

grid = [[0 for i in range(biggest)] for j in range(biggest)]
for line in lines:
  if line[0] == line[2]:
    m = min(line[1], line[3])
    M = max(line[1], line[3])
    for y in range(m, M + 1):
      grid[line[0]][y] += 1
  elif line[1] == line[3]:
    m = min(line[0], line[2])
    M = max(line[0], line[2])
    for x in range(m, M + 1):
      grid[x][line[1]] += 1
  else:
    mx = min(line[0], line[2])
    Mx = max(line[0], line[2])
    my = min(line[1], line[3])
    My = max(line[1], line[3])
    length = Mx - mx
    for i in range(length + 1):
      x = line[0] + i * (line[2] - line[0]) // length
      y = line[1] + i * (line[3] - line[1]) // length
      grid[x][y] += 1

f = open("grid.txt", "w")
for y in range(biggest):
  for x in range(biggest):
    c = grid[x][y]
    if c == 0: f.write(".")
    else: f.write(str(c))
    f.write(" ")
  f.write("\n")

danger = 0
for x in range(biggest):
  for y in range(biggest):
    if grid[x][y] >= 2: danger += 1
print "danger", danger

import sys

filename = "input.txt"

dots = []
folds = []
in_folds = False
for line in open(filename, "r"):
  line = line.strip()
  if not in_folds:
    if line == "":
      in_folds = True
    else:
      parts = line.split(",")
      dots.append((int(parts[0]), int(parts[1])))
  else:
    words = line.split()
    instruction = words[2]
    parts = instruction.split("=")
    axis = parts[0]
    number = int(parts[1])
    folds.append((axis, number))

def fold_x(dots, num):
  new_dots = []
  for (x, y) in dots:
    if x > num:
      dot = (2 * num - x, y)
    else:
      dot = (x, y)
    if dot not in new_dots:
      new_dots.append(dot)
  return new_dots

def fold_y(dots, num):
  new_dots = []
  for (x, y) in dots:
    if y > num:
      dot = (x, 2 * num - y)
    else:
      dot = (x, y)
    if dot not in new_dots:
      new_dots.append(dot)
  return new_dots

def fold(the_fold, dots):
  if the_fold[0] == "x": return fold_x(dots, the_fold[1])
  elif the_fold[0] == "y": return fold_y(dots, the_fold[1])
  else: raise "boom"

print "dots", dots
print "folds", folds

new_dots = dots
for f in folds:
  new_dots = fold(f, new_dots)

print "new dots", new_dots
width = max([x for (x, y) in new_dots])
height = max([y for (x, y) in new_dots])

for y in range(height+1):
  for x in range(width+1):
    v = "#" if (x, y) in new_dots else " "
    sys.stdout.write(v)
  print ""

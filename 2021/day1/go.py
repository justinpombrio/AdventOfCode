
last = None
counter = 0
for line in open("input.txt", "r"):
  value = int(line)
  if last != None:
    if value > last:
      print "increased"
      counter += 1
    else:
      print "decreased"
  last = value

print counter

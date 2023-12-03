
lines = []
for line in open("input.txt", "r"):
  lines.append(line.strip())
crabs = map(int, lines[0].split(","))

print "crabs", crabs

biggest = 0
for crab in crabs:
  biggest = max(biggest, crab)

print "biggest", biggest

def cost(crab, pos):
  return tri(abs(crab - pos))
def tri(n): return n * (n + 1) / 2

options = []
for pos in range(biggest + 1):
  fuel = 0
  for crab in crabs:
    fuel += cost(crab, pos)
  options.append((pos, fuel))

print "options", options

bestfuel = min([opt[1] for opt in options])
best = [opt for opt in options if opt[1] == bestfuel][0]
print "best", best

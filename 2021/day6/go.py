filename = "input.txt"
days = 256

lines = []
for line in open(filename, "r"):
  lines.append(map(int, line.strip().split(",")))

def tostate(fishes):
  state = {i: 0 for i in range(9)}
  for fish in fishes:
    state[fish] += 1
  return state

state = tostate(lines[0])

def advance(state):
  newstate = {i: 0 for i in range(9)}
  newstate[8] += state[0]
  newstate[6] += state[0]
  for n in range(0, 8):
    newstate[n] += state[n+1]
  return newstate

def count(state):
  s = 0
  for k in state:
    s += state[k]
  return s

print "Initial state:", state
for day in range(days):
  state = advance(state)
  print "After", day+1, "days:", state

print "Total:", count(state)

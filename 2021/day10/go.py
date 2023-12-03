filename = "input.txt"

chunks = []
for line in open(filename, "r"):
  chunks.append(line.strip())

def matches(x, y):
  return (x == "(" and y == ")"
    or x == "[" and y == "]"
    or x == "{" and y == "}"
    or x == "<" and y == ">")

def score(ch):
  if ch == "(": return 3
  elif ch == "[": return 57
  elif ch == "{": return 1197
  elif ch == "<": return 25137

def score2(chs):
  score = 0
  for ch in chs:
    score = score * 5
    if ch == "(": score += 1
    elif ch == "[": score += 2
    elif ch == "{": score += 3
    elif ch == "<": score += 4
  return score

scores = []
def process(chunk):
  print "processing"
  global points
  stack = []
  is_corrupt = False
  for ch in chunk:
    if ch == "(": stack.append("(")
    elif ch == "[": stack.append("[")
    elif ch == "{": stack.append("{")
    elif ch == "<": stack.append("<")
    else:
      openc = stack.pop()
      closec = ch
      if not matches(openc, closec):
        print "corrupt", openc, closec
        is_corrupt = True
        break
  if not is_corrupt and len(stack) != 0:
    print "incomplete"
    stack.reverse()
    scores.append(score2(stack))

for chunk in chunks:
  process(chunk)

scores.sort()
print "scores", scores

middle_score = scores[len(scores) // 2]
print "middle score", middle_score

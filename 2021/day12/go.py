filename = "input.txt"

graph = {}
for line in open(filename, "r"):
  parts = line.strip().split("-")
  _from = parts[0]
  _to = parts[1]
  if _from not in graph: graph[_from] = []
  graph[_from].append(_to)
  if _to not in graph: graph[_to] = []
  graph[_to].append(_from)

def has_duplicate(path):
  for i in range(len(path)):
    for j in range(i + 1, len(path)):
      x = path[i]
      y = path[j]
      if x[0].islower() and x == y:
        return True
  return False

def extend_path(path):
  end = path[-1]
  extensions = []
  for v in graph[end]:
    if (v == "start" or v == "end") and v in path:
      continue
    if has_duplicate(path) and v[0].islower() and v in path:
      continue
    extension = [x for x in path] + [v]
    print "extension", extension
    extensions.append(extension)
  return extensions

def is_done(path):
  return path[-1] == "end"

def find_all_paths():
  completed = []
  frontier = [["start"]]
  while len(frontier) != 0:
    for path in extend_path(frontier.pop()):
      if is_done(path):
        completed.append(path)
      else:
        frontier.append(path)
  return completed

print graph

all_paths = find_all_paths()
for path in all_paths:
  print "path", path

print len(all_paths)


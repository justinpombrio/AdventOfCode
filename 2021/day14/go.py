filename = "input.txt"

init_seq = ""
rewrites = {}
later = False
for line in open(filename, "r"):
  global init_seq
  line = line.strip()
  if later:
    parts = line.split(" -> ")
    rewrites[parts[0]] = parts[1]
  else:
    if line == "":
      later = True
    else:
      init_seq = line

print "init_seq", init_seq
print "rewrites", rewrites

first = init_seq[0]
last = init_seq[-1]

def score(pairs):
  d = {}
  for pair in pairs:
    n = pairs[pair]
    (x, y) = pair
    if x not in d: d[x] = 0
    if y not in d: d[y] = 0
    d[x] += n
    d[y] += n
  d[first] += 1
  d[last] += 1
  l = [(ch, d[ch]/2) for ch in d]
  l.sort(key = lambda (ch, n): n)
  return l[-1][1] - l[0][1]

# def score(seq):
#   d = {}
#   for ch in seq:
#     if ch not in d: d[ch] = 0
#     d[ch] += 1
#   l = [(ch, d[ch]) for ch in d]
#   l.sort(key = lambda (ch, n): n)
#   return l[-1][1] - l[0][1]

def seq_to_pairs(seq):
  pairs = {}
  for i in range(len(seq) - 1):
    pair = seq[i] + seq[i+1]
    if pair not in pairs: pairs[pair] = 0
    pairs[pair] += 1
  return pairs

def rewrite(pairs):
  new_pairs = {}
  for pair in pairs:
    n = pairs[pair]
    if pair in rewrites:
      ch = rewrites[pair]
      new_pair_1 = pair[0] + ch
      new_pair_2 = ch + pair[1]
      if new_pair_1 not in new_pairs: new_pairs[new_pair_1] = 0
      if new_pair_2 not in new_pairs: new_pairs[new_pair_2] = 0
      new_pairs[new_pair_1] += n
      new_pairs[new_pair_2] += n
  return new_pairs

def size(pairs):
  return sum([pairs[ch] for ch in pairs]) + 1

# def rewrite(seq):
#   new_seq = ""
#   for i in range(len(seq) - 1):
#     left = seq[i]
#     right = seq[i + 1]
#     new_seq += left
#     if left + right in rewrites:
#       new_seq += rewrites[left + right]
#   new_seq += seq[-1]
#   return new_seq

pairs = seq_to_pairs(init_seq)
print "init_pairs", pairs
for i in range(40):
  print "iter", i
  print "pairs", pairs
  pairs = rewrite(pairs)
print "final pairs", pairs
print "size", size(pairs)
print "score", score(pairs)


filename = "input.txt"

hex_table = {
  "0": [0, 0, 0, 0],
  "1": [0, 0, 0, 1],
  "2": [0, 0, 1, 0],
  "3": [0, 0, 1, 1],
  "4": [0, 1, 0, 0],
  "5": [0, 1, 0, 1],
  "6": [0, 1, 1, 0],
  "7": [0, 1, 1, 1],
  "8": [1, 0, 0, 0],
  "9": [1, 0, 0, 1],
  "A": [1, 0, 1, 0],
  "B": [1, 0, 1, 1],
  "C": [1, 1, 0, 0],
  "D": [1, 1, 0, 1],
  "E": [1, 1, 1, 0],
  "F": [1, 1, 1, 1]
}

# The input, as a list of binary digits
stream = []
for line in open(filename, "r"):
  for ch in line.strip():
    stream += hex_table[ch]

print "binary", stream

# Take and return the first n bits from the stream. This shortens the stream.
def take(n):
  global stream
  digits = stream[0:n]
  stream = stream[n:]
  return digits

# Convert a list of binary digits to a number
def tonum(digits):
  n = 0
  for digit in digits:
    n *= 2
    n += digit
  return n

def parse_packet():
  version = tonum(take(3))
  typeid = tonum(take(3))
  # Literal
  if typeid == 4:
    value = []
    while tonum(take(1)) == 1:
      value += take(4)
    value += take(4)
    value = tonum(value)
    print "literal", (version, typeid, value)
    return (version, typeid, value)
  # Operator
  else:
    if tonum(take(1)) == 0:
      # 15 bits -> length in bits of args
      length = tonum(take(15))
      print "op len", (version, typeid, length)
      streamlen = len(stream)
      args = []
      while streamlen - len(stream) < length:
        args.append(parse_packet())
      return (version, typeid, args)
    else:
      # 11 bits -> number of subpackets
      numargs = tonum(take(11))
      print "op args", (version, typeid, numargs)
      args = []
      for _ in range(numargs):
        args.append(parse_packet())
      return (version, typeid, args)

def sum_of_versions(packet):
  s = packet[0]
  if packet[1] != 4:
    for arg in packet[2]:
      s += sum_of_versions(arg)
  return s

def eval(packet):
  op = packet[1]
  if op == 4: return packet[2]
  args = map(eval, packet[2])
  if op == 0:
    s = 0
    for arg in args: s += arg
    return s
  elif op == 1:
    p = 1
    for arg in args: p *= arg
    return p
  elif op == 2:
    m = 1000000000
    for arg in args: m = min(m, arg)
    return m
  elif op == 3:
    m = -1000000000
    for arg in args: m = max(m, arg)
    return m
  elif op == 5:
    return 1 if args[0] > args[1] else 0
  elif op == 6:
    return 1 if args[0] < args[1] else 0
  elif op == 7:
    return 1 if args[0] == args[1] else 0

packet = parse_packet()
print ""
print "packet", packet
print "sum of versions", sum_of_versions(packet)
print "eval", eval(packet)
print "remaining", len(stream), stream

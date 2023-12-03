import itertools

filename = "input.txt"

data = []
for line in open(filename, "r"):
  parts = line.strip().split("|")
  inputD = parts[0].strip().split()
  outputD = parts[1].strip().split()
  data.append((inputD, outputD))

permutations = [p for p in itertools.permutations("abcdefg")]
valid = ["abcefg", "cf", "acdeg", "acdfg", "bcdf",
         "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"]

def sort(digit):
  return "".join(sorted([ch for ch in digit]))

def transform(digit, perm):
  return sort("".join(["abcdefg"[perm.index(letter)] for letter in digit]))

def toNumber(digits):
  return int("".join([str(d) for d in digits]))

outputNumbers = []
for (i, (inp, out)) in enumerate(data):
  for perm in permutations:
    success = True
    for digit in inp + out:
      if transform(digit, perm) not in valid: success = False
    if success:
      print "success", perm
      z = [valid.index(transform(digit, perm)) for digit in out]
      outputNumbers.append(toNumber(z))

print outputNumbers
print "sum", sum(outputNumbers)

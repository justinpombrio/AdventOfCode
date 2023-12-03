filename = "input.txt"

data = []
length = None
for line in open(filename, "r"):
  line = line.strip()
  number = []
  for i in range(len(line)):
    number.append(int(line[i]))
  data.append(number)

length = len(data[0])

def common(bits):
  freq = {0: 0, 1: 0}
  for bit in bits:
    freq[bit] += 1
  if freq[0] > freq[1]:
    return 0
  elif freq[1] >= freq[0]:
    return 1

def flip(bit):
  if bit == 0: return 1
  else: return 0

def filter(is_oxygen, nums):
  for i in range(length):
    if len(nums) == 1: return nums[0]
    bits = [num[i] for num in nums]
    c = common(bits)
    if not is_oxygen: c = flip(c)
    nums = [num for num in nums if num[i] == c]
  if len(nums) == 1: return nums[0]

def todecimal(num):
  n = 0
  for bit in num:
    if bit == 0:
      n = n * 2
    else:
      n = n * 2 + 1
  return n

oxygen = filter(True, data)
co2 = filter(False, data)

print oxygen
print co2

oxygenN = todecimal(oxygen)
co2N = todecimal(co2)
print oxygenN
print co2N
print oxygenN * co2N

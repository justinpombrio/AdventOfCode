
depth = []
length = 0
for line in open("input.txt", "r"):
  length += 1
  value = int(line)
  depth.append(value)

windows = []
for i in range(2, length):
  window = [depth[i-2], depth[i-1], depth[i]]
  windows.append(window)

sums = []
for window in windows:
  sums.append(sum(window))

counter = 0
for i in range(length - 2):
  print i, sum(windows[i]), sum(windows[i-1])
  if sum(windows[i]) > sum(windows[i-1]):
    counter += 1

print counter

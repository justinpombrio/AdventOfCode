
commands = []
for line in open("input.txt", "r"):
  parts = line.strip().split()
  command = (parts[0], int(parts[1]))
  commands.append(command)

pos = 0
aim = 0
depth = 0
for command in commands:
  if command[0] == "forward":
    pos += command[1]
    depth += aim * command[1]
  elif command[0] == "down":
    aim += command[1]
  elif command[0] == "up":
    aim -= command[1]
  print pos, aim, depth

print pos * depth

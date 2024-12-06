from sys import stdin

requirements = []
updates = []
for line in stdin:
    line = line.strip()
    if line == "":
        continue
    if "|" in line:
        (before, after) = line.split("|")
        requirements.append((int(before), int(after)))
    else:
        updates.append(list(map(int, line.split(","))))

def is_correct(update):
    for (before, after) in requirements:
        if before in update and after in update:
            if update.index(before) > update.index(after):
                return False
    return True

total = 0
for update in updates:
    if is_correct(update):
        print("  correct:", update)
        middle = update[(len(update) - 1) // 2]
        print("    middle", middle)
        total += middle
    else:
        print("  incorrect:", update)
print("Total:", total)

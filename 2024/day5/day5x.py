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

def put_in_order(update):
    swapped = True
    while swapped:
        swapped = False
        for page_1 in range(len(update) - 1):
            for page_2 in range(page_1, len(update)):
                if (update[page_2], update[page_1]) in requirements:
                    x = update[page_2]
                    update[page_2] = update[page_1]
                    update[page_1] = x
                    swapped = True
    return update

total = 0
for update in updates:
    if is_correct(update):
        print("  correct:", update)
    else:
        print("  incorrect:", update)
        ordered = put_in_order(update)
        print("    ordered:", ordered)
        middle = ordered[(len(ordered) - 1) // 2]
        print("    middle:", middle)
        total += middle
print("Total:", total)

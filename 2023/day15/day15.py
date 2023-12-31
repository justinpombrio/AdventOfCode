import sys

def hash(string):
    v = 0
    for ch in string:
        v += ord(ch)
        v = 17 * v
        v = v % 256
    return v

steps = []
for line in open(sys.argv[1], 'r'):
    steps = list(line.strip().split(","))

boxes = [[] for _ in range(256)]
for step in steps:
    if step.endswith("-"):
        label = step[:-1]
        box = boxes[hash(label)]
        for (i, (lens_label, lens_focal)) in enumerate(box):
            if lens_label == label:
                del box[i]
    elif "=" in step:
        (label, focus) = step.split("=")
        focus = int(focus)
        box = boxes[hash(label)]
        for (i, (lens_label, lens_focal)) in enumerate(box):
            if lens_label == label:
                box[i] = (label, focus)
                break
        else:
            box.append((label, focus))
    else:
        raise Exception("Bad step", step)

total = 0
for (i, box) in enumerate(boxes):
    print()
    print("BOX", i)
    for (j, (label, focus)) in enumerate(box):
        print(label, focus)
        total += (i + 1) * (j + 1) * focus
print("Total:", total)

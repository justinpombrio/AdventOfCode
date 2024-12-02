import sys

def is_reflection(sequence, reflection_index):
    (left, right) = (sequence[:reflection_index], sequence[reflection_index:])
    left = "".join(reversed(left))
    return left.startswith(right) or right.startswith(left)

def is_vertical_reflection(pattern, reflection_index):
    return all([is_reflection(row, reflection_index) for row in pattern])

def is_horizontal_reflection(pattern, reflection_index):
    for c in range(len(pattern[0])):
        col = "".join([row[c] for row in pattern])
        if not is_reflection(col, reflection_index):
            return False
    return True

def reflection_scores(pattern):
    for r in range(1, len(pattern[0])):
        if is_vertical_reflection(pattern, r):
            yield r
    for c in range(1, len(pattern)):
        if is_horizontal_reflection(pattern, c):
            yield 100 * c

def opposite(char):
    if char == ".":
        return "#"
    else:
        return "."

def mutations(pattern):
    for r in range(len(pattern)):
        for c in range(len(pattern[0])):
            new_pattern = [row for row in pattern]
            new_pattern[r] = pattern[r][:c] + opposite(pattern[r][c]) + pattern[r][c+1:]
            yield new_pattern

with open(sys.argv[1], 'r') as f:
    file_contents = f.read()

patterns = [section.strip().split("\n") for section in file_contents.split("\n\n")]

total = 0
for pattern in patterns:
    for row in pattern:
        print("  " + row)
    original_scores = list(reflection_scores(pattern))
    assert len(original_scores) == 1
    original_score = original_scores[0]
    print("original score:", original_score)
    print("rows:", len(pattern), "cols:", len(pattern[0]), "num mutations:",
            len(list(mutations(pattern))))
    for mutated_pattern in mutations(pattern):
        for row in mutated_pattern:
            print(" !" + row)
        scores = list(reflection_scores(mutated_pattern))
        scores = [score for score in scores if score != original_score]
        assert len(scores) <= 1
        if len(scores) == 1:
            score = scores[0]
            for row in mutated_pattern:
                print(" !" + row)
            print("final score:", score)
            total += score
            print()
            break
    else:
        print("not found!")
print("Total:", total)

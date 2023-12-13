import sys

def is_reflection(sequence, reflection_index):
    left = "".join(reversed(sequence[:reflection_index]))
    right = sequence[reflection_index:]
    return left.startswith(right) or right.startswith(left)

def is_vertical_reflection(pattern, c):
    return all([is_reflection(row, c) for row in pattern])

def column(pattern, c):
    return "".join([row[c] for row in pattern])

def is_horizontal_reflection(pattern, r):
    return all([is_reflection(column(pattern, c), r) for c in range(len(pattern[0]))])

def reflection_scores(pattern):
    for r in range(1, len(pattern[0])):
        if is_vertical_reflection(pattern, r):
            yield r
    for c in range(1, len(pattern)):
        if is_horizontal_reflection(pattern, c):
            yield 100 * c

def mutations(pattern):
    for r in range(len(pattern)):
        for c in range(len(pattern[0])):
            new_pattern = [row for row in pattern]
            smudge = "." if pattern[r][c] == "#" else "#"
            new_pattern[r] = pattern[r][:c] + smudge + pattern[r][c+1:]
            yield new_pattern

with open(sys.argv[1], 'r') as f:
    patterns = [pattern.strip().split("\n") for pattern in f.read().split("\n\n")]

total = 0
for pattern in patterns:
    for row in pattern:
        print("  " + row)
    original_score = list(reflection_scores(pattern))[0]
    for mutated_pattern in mutations(pattern):
        scores = [
            score for score in reflection_scores(mutated_pattern)
            if score != original_score
        ]
        if scores:
            print("->")
            for row in mutated_pattern:
                print("  " + row)
            print("mutated score:", scores[0])
            total += scores[0]
            print()
            break
    else:
        raise Exception("not found!")
print("Total:", total)

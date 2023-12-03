filename = "input.txt"

lines = []
for line in open(filename, "r"):
    lines.append(line.strip())

pos1 = int(lines[0][28:])
pos2 = int(lines[1][28:])

# state: (is_p1_turn, pos1, pos2, score1, score2)
# or `1` or `2` for winner

def mod10(pos):
    new_pos = pos % 10
    if new_pos == 0:
        new_pos = 10
    return new_pos

def next_states((is_p1_turn, pos1, pos2, score1, score2)):
    global wins1
    global wins2
    if score1 >= 21: return [1]
    elif score2 >= 21: return [2]
    new_states = []
    for r1 in [1, 2, 3]:
        for r2 in [1, 2, 3]:
            for r3 in [1, 2, 3]:
                roll = r1 + r2 + r3
                if is_p1_turn:
                    new_pos1 = mod10(pos1 + roll)
                    new_score1 = score1 + new_pos1
                    new_states.append((False, new_pos1, pos2, new_score1, score2))
                else:
                    new_pos2 = mod10(pos2 + roll)
                    new_score2 = score2 + new_pos2
                    new_states.append((True, pos1, new_pos2, score1, new_score2))
    return new_states

wins1 = 0
wins2 = 0
states = {(True, pos1, pos2, 0, 0): 1}
for i in range(20):
    print ""
    print "STATES", i
    for state in states:
        print "  ", state, "#", states[state]
    print "num states", len(states)
    new_states = {}
    for state in states:
        count = states[state]
        for new_state in next_states(state):
            if new_state == 1:
                wins1 += count
                continue
            elif new_state == 2:
                wins2 += count
                continue
            if new_state not in new_states:
                new_states[new_state] = 0
            new_states[new_state] += count
    states = new_states

print "wins1", wins1
print "wins2", wins2

# STATE:
#  ([0, ..., 6    -- hallway
#    8, ..., 14], -- rooms
#   dist)

import random

example_state = ([".", ".", ".", ".", ".", ".", ".",
                  "B", "A", "C", "D", "B", "C", "D", "A"],
                 0)
input_state = ([".", ".", ".", ".", ".", ".", ".",
                "D", "B", "C", "A", "D", "A", "B", "C"],
               0)
winning_state = ([".", ".", ".", ".", ".", ".", ".",
                  "A", "A", "B", "B", "C", "C", "D", "D"],
                 0)

def show_state(state):
    (state, dist) = state
    hall = state[0:7]
    room = state[7:]
    print "  #############"
    print ("  #" + hall[0] + hall[1] + "."
      + hall[2] + "." + hall[3] + "." + hall[4] + "."
      + hall[5] + hall[6] + "#")
    print ("  ###" + room[0] + "#" + room[2] + "#" + room[4]
            + "#" + room[6] + "###")
    print ("    #" + room[1] + "#" + room[3] + "#" + room[5]
            + "#" + room[7] + "#")
    print "    #########"
    print "    (" + str(dist) + ")"

show_state(example_state)

# MOVE: (src, dest, dist, obstacles)
moves = [
 (1, 2, 2, []),
 (1, 3, 4, [2]),
 (1, 4, 6, [2, 3]),
 (1, 5, 8, [2, 3, 4]),
 (1, 7, 2, []),
 (1, 9, 4, [2]),
 (1, 11, 6, [2, 3]),
 (1, 13, 8, [2, 3, 4]),

 (2, 3, 2, []),
 (2, 4, 4, [3]),
 (2, 5, 6, [3, 4]),
 (2, 7, 2, []),
 (2, 9, 2, []),
 (2, 11, 4, [3]),
 (2, 13, 6, [3, 4]),

 (3, 4, 2, []),
 (3, 5, 4, [4]),
 (3, 7, 4, [2]),
 (3, 9, 2, []),
 (3, 11, 2, []),
 (3, 13, 4, [4]),

 (4, 5, 2, []),
 (4, 7, 6, [2, 3]),
 (4, 9, 4, [3]),
 (4, 11, 2, []),
 (4, 13, 2, []),

 (5, 7, 8, [2, 3, 4]),
 (5, 9, 6, [3, 4]),
 (5, 11, 4, [4]),
 (5, 13, 2, []),

 (7, 9, 4, [2]),
 (7, 11, 6, [2, 3]),
 (7, 13, 8, [2, 3, 4]),
 
 (9, 11, 4, [3]),
 (9, 13, 6, [3, 4]),

 (11, 13, 4, [4])]

def add_behind(i, j):
    global moves
    moves += [(i, dest, dist+1, sorted([j] + ob))
              for (src, dest, dist, ob) in moves
              if src == j]
    moves += [(src, i, dist+1, sorted([j] + ob))
              for (src, dest, dist, ob) in moves
              if dest == j]
    moves += [(min(i, j), max(i, j), 1, [])]

add_behind(0, 1)
add_behind(8, 7)
add_behind(10, 9)
add_behind(12, 11)
add_behind(14, 13)
add_behind(6, 5)

# add reverses
moves += [(dest, src, dist, ob)
          for (src, dest, dist, ob) in moves]

def in_hallway(pos): return pos < 7
def in_room(pos):    return pos >= 7

def nearby_rooms(room):
    assert 7 <= room <= 14
    if room in [7, 8]: return [7, 8]
    elif room in [9, 10]: return [9, 10]
    elif room in [11, 12]: return [11, 12]
    elif room in [13, 14]: return [13, 14]
    else: raise "oops"

def is_fitting(creature, room):
    assert 7 <= room <= 14
    if creature == "A": return room in [7, 8]
    elif creature == "B": return room in [9, 10]
    elif creature == "C": return room in [11, 12]
    elif creature == "D": return room in [13, 14]
    else: raise "oops"

def move_is_legal(state, move):
    (state, score) = state
    (src, dest, dist, ob) = move
    if state[src] == "." or state[dest] != ".":
        return False
    for pos in ob:
        if state[pos] != ".":
            return False
    if in_hallway(src) and in_hallway(dest):
        return False
    if in_room(dest):
        if not is_fitting(state[src], dest):
            return False
        for room in nearby_rooms(dest):
            if state[room] != "." and state[room] != state[src]:
                return False
    if src in [8, 10, 12, 14] and is_fitting(state[src], src):
        return False
    if src in [7, 9, 11, 13] and is_fitting(state[src], src):
        if state[src + 1] == state[src]:
            return False
    if dest in [7, 9, 11, 13] and state[dest + 1] == ".":
        return False
    return True

MULTIPLIER = {"A": 1, "B": 10, "C": 100, "D": 1000}

def apply_move(state, move):
    (state, score) = state
    state = [x for x in state]
    (src, dest, dist, ob) = move
    creature = state[src]
    assert creature in ["A", "B", "C", "D"]
    state[src] = "."
    assert state[dest] == "."
    state[dest] = creature
    return (state, score + dist * MULTIPLIER[creature])

def next_states(state):
    (s, _) = state
    new_states = []
    for move in moves:
        if s[move[0]] == ".": continue
        if s[move[1]] != ".": continue
        if move_is_legal(state, move):
            new_state = apply_move(state, move)
            new_states.append(new_state)
    return new_states

def is_winning_state(state):
    (state, score) = state
    for room in range(7, 15):
        if state[room] == "." or not is_fitting(state[room], room):
            return False
    return True

def minimize(states):
    states.sort()
    distinct_states = []
    last = None
    for state in states:
        if state != last:
            distinct_states.append(state)
        last = state
    return distinct_states

def minimize_old(states):
    distinct_states = []
    for state in states:
        if state not in distinct_states:
            distinct_states.append(state)
    return distinct_states

print "moves"
for move in moves:
    print move
print "num moves", len(moves)

def run():
    states = [input_state]
    for i in range(20):
        print ""
        print "STEP", i
        print "num states", len(states)
        print "states"
        for _ in range(1):
            show_state(random.choice(states))
        print "num states", len(states)
        new_states = []
        for state in states:
            for new_state in next_states(state):
                new_states.append(new_state)
        states = minimize(new_states)
        won = False
        for state in states:
            if is_winning_state(state):
                won = True
        if won:
            states.sort(key = lambda((_, s)): s)
            for state in states:
                if is_winning_state(state):
                    (state, score) = state
                    print "winner!"
                    print "state", state
                    print "score", score
                    break

run()

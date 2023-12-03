import random
# -*- coding: utf-8 -*-

example_state = ([".", ".", ".", ".", ".", ".", ".",
                  "B", "D", "D", "A",
                  "C", "C", "B", "D",
                  "B", "B", "A", "C",
                  "D", "A", "C", "A"],
                 0,
                 None)
input_state = ([".", ".", ".", ".", ".", ".", ".",
                "D", "D", "D", "B",
                "C", "C", "B", "A",
                "D", "B", "A", "A",
                "B", "A", "C", "C"],
               0,
               None)

def show_state(state):
    (s, score, _) = state
    print "    █████████████████████████"
    print ("    █ " + s[0] + " " + s[1] + " . "
      + s[2] + " . " + s[3] + " . " + s[4] + " . "
      + s[5] + " " + s[6] + " █")
    print ("    █████ " + s[7] + " █ " + s[11] + " █ " + s[15] + " █ " + s[19] +
            " █████")
    print ("        █ " + s[8] + " █ " + s[12] + " █ " + s[16] + " █ " + s[20] +
            " █ ")
    print ("        █ " + s[9] + " █ " + s[13] + " █ " + s[17] + " █ " + s[21] +
            " █ ")
    print ("        █ " + s[10] + " █ " + s[14] + " █ " + s[18] + " █ " + s[22] +
            " █ ")
    print "        █████████████████"
    print "        (" + str(score) + ")"

def show_history(state):
    if state is None:
        return
    (_, _, history) = state
    print ""
    show_state(state)
    show_history(history)

show_state(example_state)

# MOVE: (src, dest, dist, obstacles)
moves = [
 (1, 2, 2, []),
 (1, 3, 4, [2]),
 (1, 4, 6, [2, 3]),
 (1, 5, 8, [2, 3, 4]),
 (1, 7, 2, []),
 (1, 11, 4, [2]),
 (1, 15, 6, [2, 3]),
 (1, 19, 8, [2, 3, 4]),

 (2, 3, 2, []),
 (2, 4, 4, [3]),
 (2, 5, 6, [3, 4]),
 (2, 7, 2, []),
 (2, 11, 2, []),
 (2, 15, 4, [3]),
 (2, 19, 6, [3, 4]),

 (3, 4, 2, []),
 (3, 5, 4, [4]),
 (3, 7, 4, [2]),
 (3, 11, 2, []),
 (3, 15, 2, []),
 (3, 19, 4, [4]),

 (4, 5, 2, []),
 (4, 7, 6, [2, 3]),
 (4, 11, 4, [3]),
 (4, 15, 2, []),
 (4, 19, 2, []),

 (5, 7, 8, [2, 3, 4]),
 (5, 11, 6, [3, 4]),
 (5, 15, 4, [4]),
 (5, 19, 2, []),

 (7, 11, 4, [2]),
 (7, 15, 6, [2, 3]),
 (7, 19, 8, [2, 3, 4]),
 
 (11, 15, 4, [3]),
 (11, 19, 6, [3, 4]),

 (15, 19, 4, [4])]

def add_behind(j, i):
    global moves
    moves += [(i, dest, dist+1, sorted([j] + ob))
              for (src, dest, dist, ob) in moves
              if src == j]
    moves += [(src, i, dist+1, sorted([j] + ob))
              for (src, dest, dist, ob) in moves
              if dest == j]
    moves += [(min(i, j), max(i, j), 1, [])]

add_behind(1, 0)

add_behind(7, 8)
add_behind(8, 9)
add_behind(9, 10)

add_behind(11, 12)
add_behind(12, 13)
add_behind(13, 14)

add_behind(15, 16)
add_behind(16, 17)
add_behind(17, 18)

add_behind(19, 20)
add_behind(20, 21)
add_behind(21, 22)

add_behind(5, 6)

# add reverses
moves += [(dest, src, dist, ob)
          for (src, dest, dist, ob) in moves]
moves.sort()
print "moves"
for move in moves:
    print move
print "num moves", len(moves)
print "some random moves:"
for _ in range(10):
    print random.choice(moves)


def in_hallway(pos): return pos < 7
def in_room(pos):    return pos >= 7

def nearby_rooms(room):
    assert 7 <= room <= 22
    if room in [7, 8, 9, 10]: return [7, 8, 9, 10]
    elif room in [11, 12, 13, 14]: return [11, 12, 13, 14]
    elif room in [15, 16, 17, 18]: return [15, 16, 17, 18]
    elif room in [19, 20, 21, 22]: return [19, 20, 21, 22]
    else: raise "oops"

def is_home(creature, room):
    assert 7 <= room <= 22
    if creature == "A": return room in [7, 8, 9, 10]
    elif creature == "B": return room in [11, 12, 13, 14]
    elif creature == "C": return room in [15, 16, 17, 18]
    elif creature == "D": return room in [19, 20, 21, 22]
    else: raise "oops"

def is_backmost(board, creature, dest):
    for room in nearby_rooms(dest):
        if room <= dest and board[room] != ".":
            return False
        if room > dest and board[room] != creature:
            return False
    return True

def is_in_place(board, creature, pos):
    for room in nearby_rooms(pos):
        if room < pos and board[room] != ".":
            return False
        if room > pos and board[room] != creature:
            return False
    return True

def move_is_legal(state, move):
    (board, score, _) = state
    (src, dest, dist, ob) = move
    creature = board[src]
    if board[src] == "." or board[dest] != ".":
        return False
    for pos in ob:
        if board[pos] != ".":
            return False
    if in_hallway(src) and in_hallway(dest):
        return False
    if in_room(dest):
        if src in nearby_rooms(dest):
            return False
        if not is_home(creature, dest):
            return False
        if not is_backmost(board, creature, dest):
            return False
    if in_room(src) and is_home(creature, src) and is_in_place(board, board[src], src):
        return False
    return True

MULTIPLIER = {"A": 1, "B": 10, "C": 100, "D": 1000}

def apply_move(state, move):
    (board, score, _) = state
    board = [x for x in board]
    (src, dest, dist, ob) = move
    creature = board[src]
    assert creature in ["A", "B", "C", "D"]
    board[src] = "."
    assert board[dest] == "."
    board[dest] = creature
    new_score = score + dist * MULTIPLIER[creature]
    return (board, new_score, state)

def next_states(state):
    (board, _, _) = state
    new_states = []
    for move in moves:
        if board[move[0]] == ".": continue
        if board[move[1]] != ".": continue
        if move_is_legal(state, move):
            new_state = apply_move(state, move)
            new_states.append(new_state)
    return new_states

def is_winning_state(state):
    (board, _, _) = state
    for room in range(7, 23):
        if board[room] == "." or not is_home(board[room], room):
            return False
    return True

def minimize(states):
    states.sort(key = lambda(_, score, __): score)
    states.sort(key = lambda(board, _, __): board)
    distinct_states = []
    last_board = None
    for state in states:
        (board, _, __) = state
        if board != last_board:
            distinct_states.append(state)
        last_board = board
    return distinct_states

def run():
    best = (1000000000, None)
    states = [input_state]
    for i in range(50):
        print ""
        print "STEP", i
        print "num states", len(states)
        if len(states) == 0:
            print "done"
            break
        print "random state:"
        show_state(random.choice(states))
        new_states = []
        for state in states:
            for new_state in next_states(state):
                new_states.append(new_state)
        states = minimize(new_states)
        won = False
        for state in states:
            if is_winning_state(state):
                (_, score, _) = state
                won = True
                (best_score, _) = best
                if score < best_score:
                    best = (score, state)
        if won:
            print "winner!"
    return best

bestest_winner = run()
print "bestest winner"
(score, state) = bestest_winner
print "score", score
print ""
print "HISTORY"
show_history(state)
print "score", score

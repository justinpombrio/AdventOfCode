import sys

filename = "input.txt"

board = []
for line in open(filename, "r"):
    board.append(list(line.strip()))
width = len(board[0])
height = len(board)

def step(board):
    orig_board = board
    new_board = [["." for ch in row] for row in board]
    for (r, row) in enumerate(board):
        for (c, ch) in enumerate(row):
            if ch == ".":
                continue
            elif ch == "v":
                new_board[r][c] = "v"
            elif ch == ">":
                new_c = (c + 1) % width
                if board[r][new_c] == ".":
                    new_board[r][new_c] = ">"
                else:
                    new_board[r][c] = ">"
            else: raise "oops"
    board = new_board
    new_board = [["." for ch in row] for row in board]
    for (r, row) in enumerate(board):
        for (c, ch) in enumerate(row):
            if ch == ".":
                continue
            elif ch == ">":
                new_board[r][c] = ">"
            elif ch == "v":
                new_r = (r + 1) % height
                if board[new_r][c] == ".":
                    new_board[new_r][c] = "v"
                else:
                    new_board[r][c] = "v"
    if new_board == orig_board:
        return None
    else:
        return new_board

def show_board(board):
    for row in board:
        for ch in row:
            sys.stdout.write(ch)
        print ""

show_board(board)
for i in range(500):
    print ""
    print "STEP", i+1
    new_board = step(board)
    if new_board is None:
        print "DONE", i+1
        break
    board = new_board
    show_board(board)

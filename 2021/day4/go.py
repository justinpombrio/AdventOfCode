filename = "input.txt"

lines = []
for line in open(filename, "r"):
  lines.append(line.strip())

balls = map(int, lines[0].split(","))
print "balls", balls

boards = []
board = []
for line in lines[2:]:
  if line == "":
    boards.append((board, [[False for i in range(5)] for j in range(5)]))
    board = []
  else:
    board.append(map(int, line.split()))

def winning():
  global boards
  if len(boards) == 1 and board_wins(boards[0]): return boards[0]
  boards = filter(lambda(board): not board_wins(board), boards)
  print "remaining boards:", [board[0][0][0] for board in boards]
  return None

def board_wins(board):
  for row in range(5):
    wins = True
    for col in range(5):
      if board[1][row][col] == False: wins = False
    if wins: return True
  for col in range(5):
    wins = True
    for row in range(5):
      if board[1][row][col] == False: wins = False
    if wins: return True
  return False

def cast(ball):
  for board in boards:
    for row in range(5):
      for col in range(5):
        if board[0][row][col] == ball:
          board[1][row][col] = True

def points(board):
  sum = 0
  for row in range(5):
    for col in range(5):
      if board[1][row][col] == False: sum += board[0][row][col]
  return sum

for board in boards:
  print ""
  print board

print ""
for ball in balls:
  print "cast", ball
  cast(ball)
  winner = winning()
  if winner is not None:
    print "winner!"
    print winner
    print ""
    print "sum", points(winner)
    print "points", points(winner) * ball
    break

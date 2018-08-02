import re

db = ["""
#3#|##1|#98
#9#|###|76#
##5|#7#|43#
---+---+---
###|7##|##9
8##|6#9|##7
7##|##2|###
---+---+---
#68|#4#|9##
#42|###|#1#
97#|1##|#5#
""","""
78#|#9#|###
#94|3##|###
#1#|#4#|##9
---+---+---
3#1|##4|85#
###|5#8|###
#58|7##|2#4
---+---+---
9##|#7#|#1#
###|##9|54#
###|#1#|#32
"""]

# db[0] answer is
# 783192465294356781516847329371924856429568173658731294945273618132689547867415932

def empty():
  return [[None] * 9] * 9

def digits(s):
  d = []
  for ch in s:
    if ch.isdigit():
      d.append(int(ch))
    else:
      d.append(None)
  return d

def from_line(s):
  b = []
  for row in range(9):
    b.append(digits(s[row*9:(row+1)*9]))
  return b

def from_grid(s):
  board = []
  for line in s.split("\n"):
    if re.search("[0-9#_]", line):
      digits = []
      for char in line:
        if char.isdigit():
          digits.append(int(char))
        elif char in "#_":
          digits.append(None)
      if len(digits) != 9:
        warn("Bad line:", line)
      board.append(digits)

  if len(board) > 9:
    warn(len(board), ": too many lines")

  if len(board) < 9:
    board += [[None]*9]*(9-len(lines))
  return board

def get(board_id):
  return db[board_id]

def match_line(pattern, lst):
  if len(pattern) != len(lst):
    return False

  for (p,l) in zip(pattern, lst):
    if p != None and p != l:
      return False
  return True

def matches(board, submission):
  for r in range(9):
    if not match_line(board[r], submission[r]):
      return False
  return True

def row(board, r):
  return board[r]

def col(board, c):
  col = []
  for row in board:
    col.append(row[c])
  return col

def box(board, b):
  box = []
  for x in range(3*(b//3), 3*(1+b//3)):
    for y in range(3*(b%3), 3*(1+b%3)):
      box.append(board[x][y])
  return box

def box_of(row, col):
  return 3*(row // 3) + col // 3

def constrained(lst):
  digits = set(lst)
  # We return False when there's no None so that we can ask if a row
  # is constrained when full and be told No. That is more convenient
  # for reporting interesting, "constrained" locations.
  if None not in digits:
    return False
  return len(digits) == 9       # Includes None

def contains_repeat(l):
  for i in range(len(l)):
    for j in range(len(l)):
      if i != j and l[i] != None and l[i] == l[j]:
        return True
  return False

def count(brd, digit):
  cnt = 0
  for row in brd:
    cnt += row.count(digit)
  return cnt


def advise(original, submitted):
  advice = []
  if not matches(original, submitted):
    advice.append("CHEATER!");

  for i in range(9):
    if contains_repeat(row(submitted, i)):
      advice.append("Bad Row "+str(i))
    if contains_repeat(col(submitted, i)):
      advice.append("Bad Column "+str(i))
    if contains_repeat(box(submitted, i)):
      advice.append("Bad Box "+str(i))

  for i in range(9):
    if constrained(row(submitted, i)):
      advice.append("Check Row "+str(i))
    if constrained(col(submitted, i)):
      advice.append("Check Column "+str(i))
    if constrained(box(submitted, i)):
      advice.append("Check Box "+str(i))

  for x in range(9):
    for y in range(9):
      if submitted[x][y] != None:
        continue
      all = row(submitted, x) + col(submitted, y) + \
        box(submitted, box_of(x,y))
      if constrained(set(all)):
        advice.append("Check Cell "+str((x,y)))

  for digit in range(1,10):
    if count(submitted, digit) == 8:
      advice.append("Add the last "+ str(digit));

  return advice

def to_html(board, submitted=empty()):
  squares = []
  for r in range(len(board)):
    for c in range(len(board[r])):
      box = box_of(r,c)
      entry = "known" if board[r][c] else "entry"
      content = board[r][c] or submitted[r][c] or '_'
      squares.append({'classes' : 'sq {} r{} c{} b{}'.format(entry, r, c, box),
                      'content' : content })
  return squares

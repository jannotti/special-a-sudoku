import math
import re
import sys

from . import last
from . import hint

def empty(size=9):
  return [[None] * size] * size

def digits(s):
  d = []
  for ch in s:
    if ch.isdigit():
      d.append(int(ch))
    else:
      d.append(None)
  return d

def from_line(s, size=9):
  b = []
  for row in range(size):
    b.append(digits(s[row*size:(row+1)*size]))
  return b

def from_grid(s, size=9):
  board = []
  for line in s.split("\n"):
    if re.search("[0-9#_]", line):
      digits = []
      for char in line:
        if char.isdigit():
          digits.append(int(char))
        elif char in "#_":
          digits.append(None)
      if len(digits) != size:
        warn("Bad line:", line)
      board.append(digits)

  if len(board) != size:
    warn(len(board), " lines")

  return board

def match_list(pattern, lst):
  if len(pattern) != len(lst):
    return False

  for (p,l) in zip(pattern, lst):
    if p != None and p != l:
      return False
  return True

def matches(board, submission):
  for r, row in enumerate(board):
    if not match_list(row, submission[r]):
      return False
  return True

def row(board, r):
  return board[r][:]

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
    if l[i] != None and l[i] in l[i+1:]:
      return True
  return False

def count(brd, digit):
  cnt = 0
  for row in brd:
    cnt += row.count(digit)
  return cnt

def advise(original, submitted):
  advice = []
  hints = []
  checks = []
  if not matches(original, submitted):
    advice.append("CHEATER!");

  for i in range(9):
    if contains_repeat(row(submitted, i)):
      advice.append("Bad Row "+str(i))
      checks.append(".r"+str(i))
    if contains_repeat(col(submitted, i)):
      advice.append("Bad Column "+str(i))
      checks.append(".c"+str(i))
    if contains_repeat(box(submitted, i)):
      advice.append("Bad Box "+str(i))
      checks.append(".b"+str(i))

  for i in range(9):
    if constrained(row(submitted, i)):
      advice.append("Check Row "+str(i))
      hints.append(".r"+str(i))
    if constrained(col(submitted, i)):
      advice.append("Check Column "+str(i))
      hints.append(".c"+str(i))
    if constrained(box(submitted, i)):
      advice.append("Check Box "+str(i))
      hints.append(".b"+str(i))

  for x in range(9):
    for y in range(9):
      if submitted[x][y] != None:
        continue
      all = row(submitted, x) + col(submitted, y) + \
        box(submitted, box_of(x,y))
      if constrained(all):
        advice.append("Check Cell "+str((x,y)))
        hints.append(".r"+str(x)+".c"+str(y))

  possibilities = hint.possibilities_dict(submitted)
  for n in range(1, 10):
    coords = hint.hidden_singles_row(possibilities, n)
    for coord in coords:
        advice.append("Check Cell" + str(coord) + " for " + str(n))
        hints.append(".r"+str(coord[0])+".c"+str(coord[1]))

  for n in range(1, 10):
    coords = hint.hidden_singles_col(possibilities, n)
    for coord in coords:
        advice.append("Check Cell" + str(coord) + " for " + str(n))
        hints.append(".r"+str(coord[0])+".c"+str(coord[1]))

  for n in range(1, 10):
    coords = hint.hidden_singles_box(possibilities, n)
    for coord in coords:
        advice.append("Check Cell" + str(coord) + " for " + str(n))
        hints.append(".r"+str(coord[0])+".c"+str(coord[1]))

  for digit in range(1,10):
    if count(submitted, digit) == 8:
      advice.append("Add the last "+ str(digit));

  advice.append(str(last.which_number_is_the_last_one(submitted)))

  return (advice, hints, checks)


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

class Board(object):
  def __init__(self, s=None, digits=range(1,10)):
    self.digits = digits
    self.size = len(digits)
    self.box_len = int(math.sqrt(self.size))

    if s is None:
      self.rows = empty()
    elif len(s) == self.size**2:
      self.rows = from_line(s, self.size)
    else:
      self.rows = from_grid(s)

  def __str__(self):
    return "\n".join([str(r).replace("None","_").replace(", ","")
                      for r in self.rows]);

  def get(self, r, c):
    return self.rows[r][c]
  def set(self, r, c, d):
    assert d == None or (type(d) == int and d > 0 and d < 10)
    self.rows[r][c]


  def all(self):
    return [digit for row in self.rows for digit in row]
  def row(self, r):
    return self.rows[r][:]
  def row_coords(self,r):
    return zip([r]*self.size, range(self.size))
  def col(self, c):
    return [row[c] for row in self.rows]
  def col_coords(self,c):
    return zip(range(self.size), [c]*self.size)
  def box(self, b):
    box = []
    row = self.box_len*(b//self.box_len)
    for row in self.rows[row:row+self.box_len]:
      col = self.box_len*(b%self.box_len)
      box.extend(row[col:col+self.box_len])
    return box
  def box_coords(self, b):
    coords = []
    row = self.box_len*(b//self.box_len)
    for r in range(row, row+self.box_len):
      col = self.box_len*(b%self.box_len)
      for c in range(col, col+self.box_len):
        coords.append((r,c))
    return coords
  def box_of(self, r, c):
    return self.box_len*(r // self.box_len) + c // self.box_len

  # Class function, no self
  def of(board_id):
    return Board(Board.db[board_id])


  def allows(self, submission):
    return match_list(self.all(), submission.all())

  def count(self, digit):
    return self.all().count(digit)

  def constrained(self, lst):
    digits = set(lst)
    # We return False when there's no None so that we can ask if a row
    # is constrained when full and be told No. That is more convenient
    # for reporting interesting, "constrained" locations.
    if None not in digits:
      return False
    return len(digits) == self.size # Includes None

  def missing_digit(self, lst):
    present = set(lst)
    if None not in present:
      return False
    present.remove(None)
    leftover = set(self.digits).difference(present)
    if len(leftover) != 1:
      return None
    return list(leftover)[0]

  def possibility_table(self):
    possibilities = []
    for r, row in enumerate(self.rows):
      prow = []
      for c, digit in enumerate(row):
        if digit:
          prow.append(set())
        else:
          col = self.col(c)
          box = self.box(self.box_of(r,c))
          prow.append(set(self.digits).difference(set(row+col+box)))
      possibilities.append(prow)
    return possibilities

  def hidden_singles_row(self):
    ptable = self.possibility_table()
    hints = []
    for r in range(self.size):
      prow = ptable[r]
      all_possible = [p for possibles in prow for p in possibles]
      for d in self.digits:
        if all_possible.count(d) == 1:
          for c in range(self.size):
            if d in prow[c]:
              hints.append((r, c, d))
    return hints

  def hidden_singles_col(self):
    ptable = self.possibility_table()
    hints = []
    for c in range(self.size):
      pcol = [row[c] for row in ptable]
      all_possible = [p for possibles in pcol for p in possibles]
      for d in self.digits:
        if all_possible.count(d) == 1:
          for r in range(self.size):
            if d in pcol[r]:
              hints.append((r, c, d))
    return hints

  def hidden_singles_box(self):
    ptable = self.possibility_table()
    hints = []

    for b in range(self.size):
      all_possible = []
      for r,c in self.box_coords(b):
        all_possible.extend(ptable[r][c])
      for d in self.digits:
        if all_possible.count(d) == 1:
          for r,c in self.box_coords(b):
            if d in ptable[r][c]:
              hints.append((r, c, d))
    return hints

  def advise(self, submitted):
    advice = []
    hints = [];
    checks = []
    if not self.allows(submitted):
      advice.append("CHEATER!");

    for i in range(self.size):
      if contains_repeat(submitted.row(i)):
        advice.append("Bad Row "+str(i))
        checks.append(".r"+str(i))
      if contains_repeat(submitted.col(i)):
        advice.append("Bad Column "+str(i))
        checks.append(".c"+str(i))
      if contains_repeat(submitted.box(i)):
        advice.append("Bad Box "+str(i))
        checks.append(".b"+str(i))

    for i in range(self.size):
      if self.constrained(submitted.row(i)):
        advice.append("Check Row "+str(i))
        hints.append(".r"+str(i))
      if self.constrained(submitted.col(i)):
        advice.append("Check Column "+str(i))
        hints.append(".c"+str(i))
      if self.constrained(submitted.box(i)):
        advice.append("Check Box "+str(i))
        hints.append(".b"+str(i))

    for r in range(self.size):
      for c in range(self.size):
        if submitted.get(r,c) != None:
          continue
        all = submitted.row(r) + submitted.col(c) + \
          submitted.box(submitted.box_of(r,c))
        if self.constrained(all):
          advice.append("Check Cell "+str((r,c)))
          hints.append(".r"+str(r)+".c"+str(c))

    for digit in self.digits:
      if submitted.count(digit) == self.size-1:
        advice.append("Add the last "+ str(digit));

    if self.size == 9:
      advice.append(str(last.which_number_is_the_last_one(submitted.rows)))

      for hint in self.hidden_singles_row():
        advice.append("Check Cell" + str(hint[0:2]) + " for " + str(hint[2]))
        hints.append(".r"+str(hint[0])+".c"+str(hint[1]))
    return (advice, hints, checks)

  def html(self, submitted=empty()):
    squares = []
    for r, row in enumerate(self.rows):
      for c, digit in enumerate(row):
        entry = "known" if digit else "entry"
        content = digit or submitted.get(r,c) or '_'
        squares.append({'classes' : 'sq {} r{} c{} b{}'.
                        format(entry, r, c, self.box_of(r,c)),
                        'content' : content })
    return squares

  def find_constrained_cells(self):
    cells = []
    for r in range(self.size):
      for c in range(self.size):
        if self.get(r,c) != None:
          continue
        all = self.row(r) + self.col(c) + self.box(self.box_of(r,c))
        digit = self.missing_digit(all)
        if digit != None:
          cells.append((r, c, digit))
    return cells

  def is_solved(self):
    for row in self.rows:
      if row.count(None) > 0:
        return False
    return True  
    
  def solve(self):
    progressing = True
    while not self.is_solved() and progressing:
      progressing = False
      for r, c, d in self.find_constrained_cells():
        self.rows[r][c] = d
        progressing = True
      for r, c, d in self.hidden_singles_row():
        self.rows[r][c] = d
        progressing = True
      for r, c, d in self.hidden_singles_col():
        self.rows[r][c] = d
        progressing = True
      for r, c, d in self.hidden_singles_box():
        self.rows[r][c] = d
        progressing = True
    return progressing

  def load(file_name):
    inFile = open(file_name, 'r')
    for line in inFile:
      Board.db.append(line.strip().lower())

  
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

if __name__ == "__main__":
  for file in sys.argv[1:]:
    Board.load(file)
  print("{} boards available.".format(len(Board.db)))

  for b in range(len(Board.db)):
    brd = Board(Board.db[b])
    if not brd.solve():
      print(b,"\n"+str(brd))
      print(brd.find_constrained_cells())
      print(brd.hidden_singles_box())
    
#  print(list(brd.col_coords(2)))
#  print(list(brd.row_coords(2)))
#  print(brd.box_coords(2))
#  print(brd.solve())
#  print(brd)
#  print(brd.find_constrained_cells())
  
#  print(board.advise(Board("12343___4321____", range(1,5))))
#  print(board.possibility_table())

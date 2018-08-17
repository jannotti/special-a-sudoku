import json
import math
import re
import sys

def digits(s):
  return [int(ch) if ch.isdigit() else None for ch in s]

def from_grid(s, size=9):
  board = []
  size = 0
  for line in s.split("\n"):
    if re.search("[0-9#_]", line):
      digits = []
      for char in line:
        if char.isdigit():
          digits.append(int(char))
        elif char in "#_":
          digits.append(None)
      if size != 0 and len(digits) != size:
        print("Bad line:", line)
      size = len(digits)
      board.append(digits)

  if len(board) != size:
    print(len(board), " lines")

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

def contains_repeat(l):
  for i in range(len(l)):
    if l[i] != None and l[i] in l[i+1:]:
      return True
  return False

class Hint(object):
  def __init__(self, message, interest=[], cell=None):
    self.message = message
    self.interest = interest    # a list of classes (.r3, .b2, etc)
    if type(interest) != list:  # allow one class name
      self.interest = [self.interest]
    self.cell = cell            # a tuple
  def json(self):
    return self.__dict__
  def __repr__(self):
    return json.dumps(self.__dict__)

class Board(object):
  def __init__(self, s=None):
    if type(s) == int:
      size = s
      self.rows = [[None]*s for r in range(s)]
    elif len(s) in [16,81,256]:
      size = int(math.sqrt(len(s)))
      self.rows = [digits(s[row*size:(row+1)*size])for row in range(size)]
    else:
      self.rows = from_grid(s)
      size = len(self.rows)
    self.digits = range(1, size+1)
    self.size = size
    self.box_len = int(math.sqrt(size))

  def copy(self):
    clone = Board(self.size)
    clone.rows = [row[:] for row in self.rows]
    return clone

  def __str__(self):
    return "\n".join([str(r).replace("None","_").replace(", ","")
                      for r in self.rows]);

  def get(self, r, c=None):
    if c == None:               # If a single arg is given, treat as tuple
      return self.rows[r[0]][r[1]]
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
    digits = set([self.get(coord) for coord in lst])
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
          available = set(self.digits).difference(set(row+col+box))
          if len(available) == 0:
            raise Exception("no solution")
          prow.append(available)
      possibilities.append(prow)
    return possibilities

  def unit_singles(self, ptable, coords):
    hints = []
    all_possible = []
    for r,c in coords:
      all_possible.extend(ptable[r][c])
    for d in self.digits:
      if all_possible.count(d) == 1:
        for r,c in coords:
          if d in ptable[r][c]:
            hints.append((r, c, d))
    return hints

  def hidden_singles(self):
    ptable = self.possibility_table()
    hints = []
    for i in range(self.size):
      hints.extend(self.unit_singles(ptable, self.row_coords(i)))
      hints.extend(self.unit_singles(ptable, self.col_coords(i)))
      hints.extend(self.unit_singles(ptable, self.box_coords(i)))
    return hints

  def advise(self, submitted):
    hints = [];
    checks = []

    if not self.allows(submitted):
      checks.append(Hint("CHEATER!", ".sq"));

    for i in range(self.size):
      if contains_repeat(submitted.row(i)):
        checks.append(Hint("Duplicate", ".r"+str(i)))
      if contains_repeat(submitted.col(i)):
        checks.append(Hint("Duplicate", ".c"+str(i)))
      if contains_repeat(submitted.box(i)):
        checks.append(Hint("Duplicate", ".b"+str(i)))

    for i in range(self.size):
      if submitted.constrained(submitted.row_coords(i)):
        hints.append(Hint("Row nearly done", ".r"+str(i),
                          submitted.constrained(submitted.row_coords(i))))
      if submitted.constrained(submitted.col_coords(i)):
        hints.append(Hint("Column nearly done", ".c"+str(i),
                          submitted.constrained(submitted.col_coords(i))))
      if submitted.constrained(submitted.box_coords(i)):
        hints.append(Hint("Box nearly done", ".b"+str(i),
                          submitted.constrained(submitted.box_coords(i))))

    for r in range(self.size):
      for c in range(self.size):
        if submitted.get(r,c) != None:
          continue
        all = list(submitted.row_coords(r)) + list(submitted.col_coords(c)) + \
          list(submitted.box_coords(submitted.box_of(r,c)))
        if submitted.constrained(all):
          hints.append(Hint("Check Cell "+str((r,c)),
                            ".r"+str(r)+".c"+str(c), (r,c)))

    for digit in self.digits:
      if submitted.count(digit) == self.size-1:
        for r in range(self.size):
          if submitted.row(r).count(digit) == 0:
            break
        for c in range(self.size):
          if submitted.col(c).count(digit) == 0:
            break
        hints.append(Hint("Add the last "+ str(digit), ".d"+str(digit), (r,c)))

    if self.size == 9:
      for hint in submitted.hidden_singles():
        hints.append(Hint("Hidden single in " + str(hint[0:2]),
                          ".r"+str(hint[0])+".c"+str(hint[1]), hint[0:2]))
    return (hints, checks)

  def html(self, submitted):
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
      for r, c, d in self.hidden_singles():
        self.rows[r][c] = d
        progressing = True

    if progressing:
      return self

    possibilities = self.possibility_table()
    for r, prow in enumerate(possibilities):
      for c, choices in enumerate(prow):
        if self.rows[r][c] == None:
          for choice in choices:
            copy = self.copy()
            copy.rows[r][c] = choice
            try:
              soln = copy.solve()
              if soln != None:
                return soln
            except:
              pass
    return None

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
  ""","""
  1234
  341#
  2143
  4321
  """]

  # db[0] answer is
  # 783192465294356781516847329371924856429568173658731294945273618132689547867415932

if __name__ == "__main__":
  for file in sys.argv[1:]:
    Board.load(file)
  print("{} boards available.".format(len(Board.db)))

  for b in Board.db:
    brd = Board(b)
    print(brd)
    print(brd.solve())

#  print(list(brd.col_coords(2)))
#  print(list(brd.row_coords(2)))
#  print(brd.box_coords(2))
#  print(brd.solve())
#  print(brd)
#  print(brd.find_constrained_cells())

#  print(board.advise(Board("12343___4321____", range(1,5))))
#  print(board.possibility_table())

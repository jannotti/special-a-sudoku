#!/usr/bin/env python3

import re
import sys

def warn(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

board = """
9#0|1#4|##2
#80|#60|#70
##0|##0|##0
---+---+---
4#0|##0|##1
#70|##0|#30
3#0|##0|##7
---+---+---
###|#3#|###
#30|#70|#80
1#0|2#9|##4
"""

if len(sys.argv) > 1:
  board = "\n".join(sys.argv[1:]);

lines = []
for line in board.split("\n"):
  if re.search("[0-9#_]", line):
    digits = []
    for char in line:
      if char.isdigit():
        digits.append(char)
      elif char in "#_":
        digits.append("")
    if len(digits) != 9:
      warn("Bad line:", line)
    lines.append(digits)

if len(lines) > 9:
  warn(len(lines), ": too many lines")

if len(lines) < 9:
  lines += [[""]*9]*(9-len(lines))

print(lines)

for row in range(9):
  for col in range(9):
    box = 3*(row // 3) + col // 3
    ch = lines[row][col]
    if ch.isdigit():
      kind = "known"
    else:
      kind = "entry"
    print('  <div class="sq {} b{} r{} c{}">{}</div>'
          .format(kind, box, row, col, ch))
  print('')

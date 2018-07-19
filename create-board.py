#!/usr/bin/env python3

print('<div class="board">')
for row in range(9):
  for col in range(9):
    box = 3*(row // 3) + col // 3
    print('  <div class="sq b{} r{} c{}"></div>'.format(box, row, col))
  print('')
print('</div>')


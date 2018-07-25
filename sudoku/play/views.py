from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

import re

boards = ["""
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


def index(request):
  context = {
      'boards' : boards,
  }
  template = loader.get_template('index.html')
  return HttpResponse(template.render(context, request))


def show(request, board_id):
  board = boards[board_id]
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

  context = {
    'board' : lines,
    'board_id' : board_id
  }
  template = loader.get_template('show.html')
  return HttpResponse(template.render(context, request))

def check(request):
  solution = request.GET["solution"]
  board_id = int(request.GET["board_id"])
  return HttpResponse("I'll check <b>{}</b> against <pre>{}</pre>"
                      .format(solution, boards[board_id]));


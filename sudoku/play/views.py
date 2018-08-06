from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from . import board

def index(request):
  context = {
    'boards' : board.db,
  }
  template = loader.get_template('index.html')
  return HttpResponse(template.render(context, request))

def show(request, board_id):
  brd = board.from_grid(board.get(board_id))
  submitted = board.empty()
  advice = []
  hints = []
  checks = []
  if request.POST:
    submitted = board.from_line(request.POST["solution"])
    (advice, hints, checks) = board.advise(brd, submitted)
  context = {
    'board' : brd,
    'submitted' : submitted,
    'advice' : advice,
    'hints' : hints,
    'checks' : checks,
    'squares': board.to_html(brd, submitted)
  }
  template = loader.get_template('show.html')
  return HttpResponse(template.render(context, request))


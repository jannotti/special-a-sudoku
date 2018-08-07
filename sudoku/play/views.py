from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .board import Board

def index(request):
  context = {
    'boards' : Board.db,
  }
  template = loader.get_template('index.html')
  return HttpResponse(template.render(context, request))

def show(request, board_id):
  brd = Board.of(board_id)
  submitted = Board()
  advice = []
  hints = []
  checks = []
  if request.POST:
    submitted = Board(request.POST["solution"])
    (advice, hints, checks) = brd.advise(submitted)
  context = {
    'advice' : advice,
    'hints' : hints,
    'checks' : checks,
    'squares': brd.html(submitted)
  }
  template = loader.get_template('show.html')
  return HttpResponse(template.render(context, request))

from django.core.serializers.json import DjangoJSONEncoder
#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader


from .board import Board

if len(Board.db) < 10:
  Board.load("play/easy.txt")
  Board.load("play/hard.txt")
  Board.load("play/hardest.txt")

def index(request):
  context = {
    'boards' : Board.db,
  }
  template = loader.get_template('index.html')
  return HttpResponse(template.render(context, request))

def show(request, board_id):
  brd = Board.of(board_id)
  submitted = brd.copy()
  hints = []
  checks = []
  time = 0
  if request.POST:
    submitted = Board(request.POST["solution"])
    time = int(request.POST["time"])
    (hints, checks) = brd.advise(submitted)
  context = {
    'hints' : hints,
    'checks' : checks,
    'squares': brd.html(submitted),
    'time' : time,
  }
  template = loader.get_template('show.html')
  return HttpResponse(template.render(context, request))

class JsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
      try:
        return obj.json()
      except AttributeError:
        return super().default(obj)

def hint(request, board_id):
  brd = Board.of(board_id)
  submitted = brd.copy()
  hints = []
  checks = []
  if request.POST:
    submitted = Board(request.POST["solution"])
    (hints, checks) = brd.advise(submitted)
  context = {
    'hints' : hints,
    'checks' : checks,
    'rows' : brd.solve().rows
  }
  return JsonResponse(context, JsonEncoder)

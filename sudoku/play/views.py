from django.shortcuts import render

from django.http import HttpResponse

def index(request):
  return HttpResponse("This could list playable boards.")

def show(request, board_id):
  return HttpResponse("This would show board {}.".format(board_id))

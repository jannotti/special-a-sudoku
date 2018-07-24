from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

def index(request):
  return HttpResponse("This could list playable boards.")

def show(request, board_id):
  return HttpResponse("This would show board {}.".format(board_id))

def sample(request):
    template = loader.get_template('sample.html')
    context = {
        'leading_text': "This could be anything",
    }
    return HttpResponse(template.render(context, request))

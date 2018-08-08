from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show/<int:board_id>', views.show, name='show'),
    path('hint/<int:board_id>', views.hint, name='hint'),
]

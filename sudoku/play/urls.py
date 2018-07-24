from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:board_id>', views.show, name='show_a_board'),
    path('sample', views.sample, name='sample'),
]

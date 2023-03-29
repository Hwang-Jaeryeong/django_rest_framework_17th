from django.urls import path
from .views import board_list, board_write, board_detail
urlpatterns = [
    path('list/', board_list, name='board_list'),
    path('write/', board_write, name='board_write'),
    path('detail/<int:pk>/', board_detail, name='board_detail'),
]


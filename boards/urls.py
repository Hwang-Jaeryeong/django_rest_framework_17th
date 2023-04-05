from django.urls import path
from .views import board_list, board_write, board_detail, comment_write
from . import views

urlpatterns = [
    path('list/', board_list, name='board_list'),
    path('write/', board_write, name='board_write'),
    path('comment_write/<int:board_id>', comment_write, name = "comment_write"),
    path('detail/<int:pk>/', board_detail, name='board_detail'),
    path('api/board/', views.BoardList.as_view()),
    path('api/board/<int:pk>/', views.BoardDetail.as_view()),
    path('api/comment/', views.CommentList.as_view()),
    path('api/comment/<int:pk>/', views.CommentDetail.as_view())
]


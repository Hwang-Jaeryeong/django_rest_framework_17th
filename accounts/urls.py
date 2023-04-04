from django.urls import path
from .views import register, login, logout
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('api/', views.UserList.as_view()),
    path('api/<int:pk>/', views.UserDetail.as_view())
]
# 임포트한 views.py에서 생성했던 register, login, logout 함수를 임포트해준뒤 각각을 연결
# name은 나중에 템플릿이나 view에서 유용하게 사용
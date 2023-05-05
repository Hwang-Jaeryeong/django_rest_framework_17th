from django.urls import path, include
from .views import register, login, logout, UserViewSet, AuthView
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    # path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    # path('api/', views.UserList.as_view()),
    # path('api/<int:pk>/', views.UserDetail.as_view()),
    # path('api/', include(router.urls)),
    path("auth/", AuthView.as_view()),
]


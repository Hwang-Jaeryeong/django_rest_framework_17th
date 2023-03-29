from django.urls import path
from .views import TimetableListCreate, FriendListCreate

urlpatterns = [
    path('timetable/', TimetableListCreate.as_view(), name='timetable'),
    path('friend/', FriendListCreate.as_view(), name='friend'),
]
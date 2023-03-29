from django.urls import path
from . import views

app_name = 'timetable'
urlpatterns = [
    path('time/', views.timetable_index, name='timetable_index'),
]
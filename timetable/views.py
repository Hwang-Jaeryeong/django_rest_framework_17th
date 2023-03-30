from rest_framework import generics
from .models import Timetable, Friend, Subject
from .serializers import TimetableSerializer, FriendSerializer, SubjectSerializer

class TimetableListCreate(generics.ListCreateAPIView):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer

class SubjectListCreate(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class FriendListCreate(generics.ListCreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


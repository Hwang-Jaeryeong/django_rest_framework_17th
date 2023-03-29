from rest_framework import serializers
from .models import Timetable, Friend

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ['id', 'user', 'subject', 'day', 'start_time', 'end_time']

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ['id', 'user', 'friend']

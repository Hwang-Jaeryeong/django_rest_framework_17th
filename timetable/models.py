from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.teacher}) {self.code}"

class Timetable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username}: {self.subject.name} ({self.get_day_display()}) {self.start_time}-{self.end_time}"

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"

# 위 코드에서, Subject 모델은 수업의 이름, 교사, 코드 등을 저장하며,
# Timetable 모델은 특정 사용자가 어떤 수업을 어떤 날에 언제부터 언제까지 듣는지를 저장합니다.
# 마지막으로, Friend 모델은 사용자와 그의 친구를 연결하는데 사용됩니다.

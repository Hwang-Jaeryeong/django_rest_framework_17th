from django.db import models
from django.contrib.auth.models import User


class User(models.Model):  # 1
    # 유니크 제약 조건 사용 추가
    username = models.CharField(max_length=700, unique=True)
    useremail = models.EmailField(max_length=700, unique=True)
    password = models.CharField(max_length=600)
    # user가 생성된 바로 그 시간에 저장됨
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now=True는 수정된 시간을 나타냄(board 모델 작성할 때 쓰이게 됨)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): # 2
        return self.username

    class Meta: # 3
        db_table = 'community_user'
        verbose_name = '커뮤니티 사용자'
        verbose_name_plural = '커뮤니티 사용자'
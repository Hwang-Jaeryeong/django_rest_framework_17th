from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username, password, nickname, **extra_fields):
        if not username:
            raise ValueError('username Required!')

        user = self.model(
            username=username,
            nickname=nickname,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, nickname=None):
        user = self.create_user(username, password, nickname)

        user.is_superuser = True
        user.is_staff = True
        user.level = 0

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(primary_key=True, max_length=17, verbose_name="id", unique=True)

    username = models.CharField(max_length=17, verbose_name="아이디", unique=True)
    nickname = models.CharField(max_length=100, verbose_name="이름", null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # 유저 대학교

    def __str__(self):
        return self.username 
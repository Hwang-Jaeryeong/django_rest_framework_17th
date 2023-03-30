from django.contrib import admin
from .models import User

admin.site.register(User)
# .models -> 현재 폴더 내의 models 파일로부터 User 클래스를 임포트 해와서 사이트를 등록

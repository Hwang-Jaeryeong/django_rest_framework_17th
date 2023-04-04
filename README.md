# CEOS 17기 백엔드 스터디

https://confused-cantaloupe-b70.notion.site/2-_-0eaa6b8bd3374782ad5299e8ce6a27ac
: 사진이나 첨부파일(ERD)가 노션에 포함되어 있어 첨부했습니다 !


* 서비스 설명
  * accounts 앱 : 로그인/로그아웃/회원가입
  
```
 from django.db import models
 from django.contrib.auth.models import User

 class User(models.Model): 
    username = models.CharField(max_length=1000)
    useremail = models.EmailField(max_length=1000)
    password = models.CharField(max_length=1000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'community_user'
        verbose_name = '커뮤니티 사용자'
        verbose_name_plural = '커뮤니티 사용자'
```

  * boards 앱 : 게시판에 글쓰기/모든 게시물 보기(list)/댓글 달기/목록에서 클릭한 게시물보기(list)
```
 from django.db import models

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    tags = models.ManyToManyField('tag.Tag')
    writer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'boards'
        verbose_name = '커뮤니티 게시판'
        verbose_name_plural = '커뮤니티 게시판'


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Board', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
```
  * tag 앱 : 태그 (게시글을 작성할 때 그 글이 포함되어 있는 내용을 단어로 요약. 입력받은 값을 저장하되 기존에 겹치는 태그는 늘리지 저장이 아닌 불러오는 형식)
```
from django.db import models

# Create your models here.

class Tag(models.Model):
    name =models.CharField(max_length=100, verbose_name='태그명')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'community_tag'
        verbose_name = '태그'
        verbose_name_plural = '태그'
```

  * timetable 앱 : 시간표 짜기/친구맺기/과목 등록하기

```
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
```
user필드는 친구 관계를 맺는 사용자, friend필드는 해당 사용자의 친구

* 새롭게 알게 된 것
  * ModelForm 방식 (in boards/forms.py)
    * 폼이 알아서 model에 선언되어있는 comment필드에 맞춰 폼 형식을 생성. 기존의 복잡하고 귀찮던 코드들이 간결해짐.
  * urls.py
    * 실질적인 html 파일이 존재하지는 않음. 그러나 boards/comment_write/<int:board_id>로 값이 보내짐
  * workbench로 ERD Diagram 생성하기
    * **1. workbench에서 데이터베이스 선택하여 Reverse 시작**

    * **2. 개체 생성하기**

    * **3. 테이블 관계 설정하기**

    * **4. 테이블 완성**

    * **5. database > forward 를 통해 코드 내보내기 (사용하기 위해)**
* 오류 해결
  *  .env 파일에서 자꾸 에러가 났었는데 몇 개 install하니 서버는 실행되었지만 에러가 없어지지 않았습니다. 코드 자체의 에러가 아니라 확장자 인식을 못한 거였습니다. 
     * **해결방법** : .env 파일 -> Override file type -> dotENV 하니 에러 해결되었습니다 !
  *  **django.db.utils.DataError: (1406, "Data too long for column 'password' at row 1")** : 비밀번호 길이가 너무 길어서 생긴 오류
     * **해결방법** : max_length값을 변경하고 makemigrations와 migrate를 다시 해주니 해결되었습니다
  * Unresolved reference ‘commnent_write’ : 댓글 작성 폼을 담은 변수명이 commnent_write로 되어 있어서, 폼을 검증하는 부분에서 if comment_write.is_valid():이 잘못된 변수명인 것 !! 이로 인해 comment_write 변수가 정의되지 않았다는 에러가 발생했던 것이다.
     * **해결방법** : if comment_write_form.is_valid(): 로 바꾸어 해결
  * MultipleObjectsReturned at /accounts/login/
     * **해결방법** : unique=True 필드가 중복된 데이터를 방지하는 필드 / 이미 중복된 데이터가 생성된 경우, 이를 삭제
* ORM 이용해보기 과제 //
모델링 할 때도 쿼리문을 사용하였다. (timetable 앱의 views.py)

```
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
```
* Django REST framework의 generics 모듈을 사용하여 ListCreateAPIView를 구현
* ListCreateAPIView 클래스는 GET 요청을 받으면 queryset 속성에 설정된 모델의 모든 인스턴스를 시리얼라이저를 사용하여 JSON 형태로 반환하고, POST 요청을 받으면 전달된 데이터를 기반으로 새 인스턴스를 생성하고 시리얼라이저를 사용하여 JSON 형태로 반환
* TimetableListCreate, SubjectListCreate, FriendListCreate는 각각 Timetable, Subject, Friend 모델에 대한 ListCreateAPIView를 구현. queryset 속성에는 모델의 모든 인스턴스를 가져오기 위해 objects.all()이 설정되고, serializer_class 속성에는 해당 모델에 대한 시리얼라이저 클래스가 설정.
* TimetableSerializer, FriendSerializer, SubjectSerializer는 models.py에서 정의된 Timetable, Friend, Subject 모델에 대한 시리얼라이저이다. 시리얼라이저는 모델 인스턴스를 JSON 형식으로 직렬화하고, 역직렬화하여 JSON 데이터를 모델 인스턴스로 변환

* → timetable.models Subject, Timetable, Friend 중 Friend 선택
### 1. 데이터베이스에 해당 모델 객체 3개 이상 넣기
코드
```
from django.contrib.auth.models import User
from timetable.models import Friend

user1 = User.objects.create_user(username='user1', password='iluvu')
user2 = User.objects.create_user(username='user2', password='metoo')
user3 = User.objects.create_user(username='user3', password='jryeong')

friend1 = Friend.objects.create(user=user1, friend=user2)
friend2 = Friend.objects.create(user=user2, friend=user3)
friend3 = Friend.objects.create(user=user1, friend=user3)
```

### 2. 삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)
코드
```
Friend.objects.all()
```
결과
```
<QuerySet [<Friend: jaeryeong is friend with jaeryeong>, <Friend: user1 is friend with user2>, <Friend: user1 is friend with user3>, <Friend: user2 is friend with user3>]>
```

### 3. filter 함수 사용해보기
코드
```
Friend.objects.filter(user=user3)
```

결과
```
<QuerySet [<Friend: user3 is friends with user1>, <Friend: user3 is friends with user2>]>
```


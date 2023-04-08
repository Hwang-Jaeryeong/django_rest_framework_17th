# CEOS 17기 백엔드 스터디


## CBV로 API 만들기
  * User
  1) URL : accounts/api/
  2) Method : GET   :  accounts/api/ GET
  
  
```
   [
    {
        "id": 1,
        "username": "홍한",
        "useremail": "andyj0927@kaist.ac.kr",
        "password": "pbkdf2_sha256$260000$wDRdVl1K64ukO0F9BRmThG$m4PBhq6XQLg8IhTpKBB8QHlF0Og+cA2LNEc7nMj3XsQ=",
        "created_at": "2023-03-31T20:57:57.107502+09:00",
        "updated_at": "2023-03-31T20:57:57.107502+09:00"
    },
    {
        "id": 2,
        "username": "재령",
        "useremail": "jrjwjy@naver.com",
        "password": "pbkdf2_sha256$260000$ZOrdbXrInxAqpErypYnHp2$QCM3lwEg4CK68FTFnBJFxtJRQWe9TML8AkTMJ1U/34c=",
        "created_at": "2023-03-31T20:58:49.109280+09:00",
        "updated_at": "2023-03-31T20:58:49.109280+09:00"
    }
]
```

  * 특정 데이터를 가져오는 API 만들기
    
    1) URL : accounts/api/<int:pk>/
    2) Method : GET   :  : accounts/api/2/ GET
```
 {
    "id": 2,
    "username": "재령",
    "useremail": "jrjwjy@naver.com",
    "password": "pbkdf2_sha256$260000$ZOrdbXrInxAqpErypYnHp2$QCM3lwEg4CK68FTFnBJFxtJRQWe9TML8AkTMJ1U/34c=",
    "created_at": "2023-03-31T20:58:49.109280+09:00",
    "updated_at": "2023-03-31T20:58:49.109280+09:00"
}
```
  * 새로운 데이터를 create하도록 요청하는 API 만들기
    1) URL : accounts/api/
    2) Method : POST
    3) Body:
```
{
        "id": 5,
        "username": "새로운 유저",
        "useremail": "new@naver.com",
        "password": "new1111",
        "created_at": "2023-04-06T23:02:07.391585+09:00",
        "updated_at": "2023-04-06T23:02:07.391585+09:00"
    }
```

  * 특정 데이터를 삭제 또는 업데이트하는 API
    1) URL : accounts/api/<int:pk>/
    2) Method : `DELETE` : :accounts/api/3/ DELETE
    <img src="./img/user delete 6.jpg">
    <img src="./img/delete 결과.jpg">


## 새롭게 알게 된 것
  * Json 형식으로 보는 법
```
  REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
```

  * 인터페이스 형식으로 보는 법
```
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.Renderer',
    )
}
```

## Viewset으로 리팩토링하기
Board, Comment Viewset
```
class BoatdViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Board.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoardFilter

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
```
URL 매핑
```
router = routers.DefaultRouter()
router.register(r'board', BoardViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
```

### filter 기능 구현하기
BoardFliter
```
class BoardFilter(FilterSet):
    writer = filters.CharFilter(method='filter_user')
    contents = filters.CharFilter(field_name='contents', lookup_expr='icontains')

    class Meta:
        model = Board
        fields = ['writer', 'contents']

    def filter_user(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })
```

## 내용 정리
filter()의 조건 키워드
### 키워드 앞에 쓰이는 `__`

- 조건을 사용할 떄
- 외부 모델 필드를 사용할 때
### contains / icontains

지정한 문자열을 포함하는 자료 검색

`queryset.filter(title__contains='hi')`

`queryset.filter(title__icontains='hi')` icontains는 대소문자 구별하지 않음

### exact / iexact

정확히 일치하는 자료 검색

`queryset.filter(title__exact='hi')`

`queryset.filter(title__iexact='hi')` iexact는 대소문자 구별하지 않음

### startswith / endswith

지정한 문자열로 시작하는[끝나는] 자료 검색

`queryset.filter(title__startswith='hihi')`

`queryset.filter(title__istartswith='hihi')` istartswith는 대소문자 구별하지 않음

**회고**

View를 계속 리팩토링하는 것이 코드의 길이가 줄어드는 게 보여서 장고가 간단하고 편리한 툴이라고 다시 생각했다 !

시험기간이라서 뭔가 촉박하게 과제를 마무리한 것 같은데 다음 과제부터는 공부도 꼼꼼하게 하면서 많은 기능들을 더 많이 구현해보고 싶다
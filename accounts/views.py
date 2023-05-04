from django.shortcuts import render, redirect
from .models import User
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status, viewsets
from .serializers import UserSerializer
from django_filters import rest_framework as filters, FilterSet
from django.core import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication





class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserFilter(FilterSet):
    user = filters.CharFilter(method='filter_user')

    class Meta:
        model = User
        fields = ['username',]

    def filter_user(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

"""
class UserList(APIView):

    def user(self, request, format=None):
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# 로그인을 했는지 안했는지 알아보기위해 홈화면 간단하게 구성
def home(request):
    user_id = request.session.get('username')
    if user_id:
        user = User.objects.get(pk=user_id).first()
        if user:
            return HttpResponse("안녕하세요 %s님" % user)
        else:
            return HttpResponse("프로필이 존재하지 않습니다!")
    else:
        return HttpResponse("로그인 후 이용해주세요!")

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')


    elif request.method == 'POST':
        username = request.POST.get('username', None)
        #useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        err_data = {}
        if not (username and useremail and password and re_password):
            err_data['error'] = '모든 값을 입력해주세요.'

        elif password != re_password:
            err_data['error'] = '비밀번호가 다릅니다.'

        else:
            user = User(
                username=username,
                useremail=useremail,
                password=make_password(password),
            )
            user.save()
        return render(request, 'register.html', err_data)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # is_valid : forms.py의 유효성 검사를 모두 거쳐야지 다음의 조건을 수행하도록 해준다는 함수
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    if request.session.filter('user'):
        del (request.session['user'])
    return redirect('/')

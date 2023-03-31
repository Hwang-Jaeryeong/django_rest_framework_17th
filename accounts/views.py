from django.shortcuts import render, redirect
from .models import User
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

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
        useremail = request.POST.get('useremail', None)
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
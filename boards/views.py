
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BoardSerializer, CommentSerializer
from tag.models import Tag
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from accounts.models import User
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend




class BoardList(APIView):
    def board(self, request, format=None):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset = Board.objects.all()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)


class BoardDetail(APIView):
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        board = self.get_obkect(pk)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        board = self.get_object(pk)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    def comment(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comment = self.get_obkect(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def board_write(request):
    if not request.session.get('user'):
        return redirect('/accounts/login')

    if request.method =='POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            user = User.objects.get(pk=user_id)
            tags = form.cleaned_data['tags'].split(',')

            board=Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = user
            board.save()

            for tag in tags:
                if not tag:
                    continue
                _tag, _ = Tag.objects.get_or_create(name=tag)
                board.tags.add(_tag)

            return redirect('/boards/list')
    else:
        form = BoardForm()
    return render(request, 'board_write.html', {'form':form})

# def board_detail(request, pk):
    # board = get_object_or_404(Board, pk=pk)
    # return render(request, 'board_detail.html',{'board':board})

def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comments = CommentForm()
    comment_view = Comment.objects.filter(post=pk)
    return render(request, 'board_detail.html',{'board':board, 'comments':comments, 'comment_view':comment_view})

def board_list(request):
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 5)
    boards = paginator.get_page(page)

    return render(request, 'board_list.html', {'boards':boards})

def comment_write(request, board_id):
    comment_write = CommentForm(request.POST)
    user_id = request.session['user']
    user = User.objects.get(pk=user_id)
    if comment_write.is_valid():
        comments = comment_write.save(commit=False)
        comments.post = get_object_or_404(Board, pk=board_id)
        # pk를 추가해준것은 게시글 각각의 id값을 통해 board_detail url을 구분해주기위해 추가
        comments.author = user
        comments.save()
    return redirect('board_detail', board_id)






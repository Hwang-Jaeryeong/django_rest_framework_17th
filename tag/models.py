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


# 태그 기능 : 게시글을 작성할 때 그 글이 포함되어 있는 내용을 단어로 요약
# 게시글을 작성할 때마다 개수 제한 없이 태그를 입력받을 수 있다.
# 입력받은 값을 저장하되 기존에 겹치는 태그는 늘리지 저장이 아닌 불러오는 형식
from django.db import models
from django.urls import reverse

# 导入内建的user模型
from django.contrib.auth.models import User

# timezone用于处理时间相关事务
from django.utils import timezone


class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# Create your models here.
class ArticlePost(models.Model):

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    likes = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    body = models.TextField()

    total_views = models.PositiveIntegerField(default=0)

    # 在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

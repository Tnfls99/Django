from django.db import models
from django.contrib.auth.models import User
import os
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model): ## Model 업그레이드 할 때마다 migrate 잊지 말기
    ## 필드선언하는곳
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self): # post로 만들어진 오브젝트 하나하나를 의미
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self): ## 파일 이름을 가져오는 것
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self): ## 파일 학장자 가져오는 것
        return self.get_file_name().split('.')[-1] ## -1로 가장 마지막 문자인 확장자를 가져옴

    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model): #블로그 포스트가 존재해야만 댓글을 달 수 있다. 댓글과 포스트는 다대일 관계
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 포스트가 삭제되면 댓글도 모두 삭제
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 한명의 유저가 여러개의 댓글을 달 수 있기 때문에 다대일 관계
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://doitdjango.com/avatar/id/426/215f50b97258a737/svg/{self.author.email}/'

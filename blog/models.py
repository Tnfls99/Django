from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model): ## Model 업그레이드 할 때마다 migrate 잊지 말기
    ## 필드선언하는곳
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #author
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self): # post로 만들어진 오브젝트 하나하나를 의미
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self): ## 파일 이름을 가져오는 것
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self): ## 파일 학장자 가져오는 것
        return self.get_file_name().split('.')[-1] ## -1로 가장 마지막 문자인 확장자를 가져옴
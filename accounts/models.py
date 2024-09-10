from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    name = models.CharField(max_length=150, verbose_name='이름')
    nickname = models.CharField(
        max_length=50, unique=True, null=True, blank=True)  # 닉네임
    birthday = models.DateField(null=True, blank=True)  # 생일
    gender = models.CharField(max_length=10, choices=[('M', '남성'), ('F', '여성'), ('O', '기타')], blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # 자기소개 (생략가능)
    email = models.EmailField(unique=True)  # 이메일 (유일)

    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='following', blank=True)  # 팔로잉 시스템

    ## 영어식이름 삭제 후 새로운 name 필드 생성
    first_name = None
    last_name = None

    def __str__(self):
        return self.username

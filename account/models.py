from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 让用户添加手机号码
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# 添加更多个人信息
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True) #unique为true即只能有一个
    school = models.CharField(max_length=100, blank=True)   #blank即用户在前端可以不写
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True) #头像可以为空

    def __str__(self):
        return "user:{}".format(self.user.username)
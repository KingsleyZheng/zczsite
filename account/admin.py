from django.contrib import admin
from .models import UserProfile, UserInfo

# Register your models here.
# 在超级管理员界面对自己添加的信息集中管理
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth', 'phone')
    list_filter = ("phone",)

# 在超级管理员界面对自己添加的信息集中管理2
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "company", "profession", "address", "aboutme", "photo")
    list_filter = ("school", "company", "profession")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
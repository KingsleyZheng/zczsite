from django.contrib import admin
from .models import ArticleColumn

# Register your models here.
# 将管理权限赋予超级管理员
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'created', 'user')
    list_filter = ('user',)

admin.site.register(ArticleColumn, ArticleColumnAdmin)
#建立用户添加文章的form类型
from django import forms
from .models import ArticleColumn, ArticlePost, Comment
from .models import ArticleTag

# 创建栏目的表单
class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",) #数据库记录的字段

# 用户创建文章时显示的表单
class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'body')

# 对文章进行评论的表格
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator", "body",) #created是自动生成

# 标签的表单
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('tag',)
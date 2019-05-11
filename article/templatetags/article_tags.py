#统计文章总数
from django import template
register = template.Library()

from article.models import ArticlePost

from django.db.models import Count

#所有文章数
@register.simple_tag 
def total_articles():
    return ArticlePost.objects.count()

#作者文章数
@register.simple_tag
def author_total_articles(user):
    return user.article.count()

#最新发布的文章
@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles": latest_articles}

#评论最多的文章
@register.simple_tag
def most_commented_articles(n=3):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by("-total_comments")[:n]

# 编写将Markdown编码转换为HTML代码的函数
from django.utils.safestring import mark_safe #编码为字符串
import markdown

@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))
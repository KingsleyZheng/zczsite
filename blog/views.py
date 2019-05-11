from django.shortcuts import render, get_object_or_404
from .models import BlogArticles

# Create your views here.
#读取文章标题列表
def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/titles.html", {"blogs":blogs}) # render函数的作用是将数据渲染到指定模板上

#获取文章内容
def blog_article(request, article_id):
    #article = BlogArticles.objects.get(id=article_id)\
    article = get_object_or_404(BlogArticles, id=article_id)
    pub = article.publish
    return render(request, "blog/content.html", {"article":article, "publish":pub})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django .views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# 从编写的文件中引入
from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm
# 分页
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# 文章标签
from .models import ArticleTag
from .forms import ArticleTagForm
import json

# Create your views here.
# 构建用户后台管理的视图函数
# 添加栏目的视图函数
@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user) #筛选出该用户的所有条目
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns":columns, "column_form":column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name) #没有当前用户创建的该栏目才允许创建
        if columns:
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")

# 修改栏目的视图函数
@login_required(login_url='/account/login/')
@require_POST #保证此视图函数只接收通过POST方式提交的函数
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

# 删除栏目的视图函数
@login_required(login_url='/account/login/')
@require_POST #保证此视图函数只接收通过POST方式提交的函数
@csrf_exempt
def del_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

# 用户创建文章的视图函数
@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid(): #符合限定的各种field
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False) #先不保存到数据库，以节省时间
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse('1')
            except:
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else: #GET
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        return render(request, "article/column/article_post.html", {"article_post_form":article_post_form, "article_columns":article_columns, "article_tags":article_tags})

# 查看用户文章列表的视图函数 增加分页
@login_required(login_url='/account/login/')
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user) #筛选出当前登录用户发布的所有文章
    paginator = Paginator(articles_list, 5) #每页最多两个
    page = request.GET.get('page') #request中的页码
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages) #最后一页
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles":articles, "page":current_page})

# 查看用户文章内容的视图函数
@login_required(login_url='/account/login/')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article":article})

# 删除用户文章的视图函数
@login_required(login_url='/account/login/')
@require_POST #保证此视图函数只接收通过POST方式提交的函数
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')

# 修改用户文章的视图函数
@login_required(login_url='/account/login/')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title":article.title})
        this_article_column = article.column
        return render(request, "article/column/redit_article.html",{"article":article,"article_columns":article_columns, "this_article_column":this_article_column,"this_article_form":this_article_form})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except:
            return HttpResponse('2')

# 增加或显示文章标签
@login_required(login_url='/account/login/')
@csrf_exempt
def article_tag(request):
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm
        return render(request, "article/tag/tag_list.html", {"article_tags":article_tags,"article_tag_form":article_tag_form})
    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")
            except:
                return HttpResponse('保存tag失败。')
        else:
            return HttpResponse('抱歉，数据无效。')

# 删除文章标签
@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")
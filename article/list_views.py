from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost
# 按作者查看文章
from django.contrib.auth.models import User
# 点赞功能
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# 与redis数据库建立连接
import redis
from django.conf import settings
# 引入文章评论功能
from .models import Comment
from .forms import CommentForm
# 推荐相似文章
from django.db.models import Count

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# 新查看文章列表页
def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try: #在内容页显示作者个人信息
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list

    if username:
        return render(request, "article/list/author_articles.html", {"articles":articles, "page":current_page, "userinfo":userinfo, "user":user})
    return render(request, "article/list/article_titles.html", {"articles":articles, "page":current_page})

# 游客端新查看文章内容页 不要求登录
def article_detail(request, id, slug): #不要求登录
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id)) #incr即让键值递增  对象类型：对象ID：对象属性
    r.zincrby('article_ranking', 1, article.id) #排序

    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10] #得到排序中前十的文章id
    article_ranking_ids = [int(id) for id in article_ranking] #将id变为int
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids)) #查询出id在idranking中的所有文章对象并形成列表
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id)) #按照list中id（list后乱序了）在ranking中的index对list排序
    # 引入评论功能
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)#先不保存
            new_comment.article = article
            new_comment.save()
    else: #GET
        comment_form = CommentForm()
        article_tags_ids = article.article_tag.values_list("id", flat=True)
        similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
        similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]
    return render(request, "article/list/article_content.html", {"article":article, "total_views":total_views, "most_viewed":most_viewed, "comment_form":comment_form, "similar_articles":similar_articles})

# 点赞文章
@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id") #从request获取文章id 前端必须以类字典的形式向视图函数提交数据
    action = request.POST.get("action") #从request获取用户动作
    if article_id and action: #以上两者都有
        try: 
            article = ArticlePost.objects.get(id=article_id) #根据ID从数据库提取文章
            if action == "like": 
                article.users_like.add(request.user) #在users_like类加上该user
                return HttpResponse("1") #响应成功点赞
            else: 
                article.users_like.remove(request.user) #移除该user
                return HttpResponse("2") #响应成功取消点赞
        except:
            return HttpResponse("no") #数据库中找不到该文章
from django.db import models
from django.contrib.auth.models import User
# 文章数据类型
from django.utils import timezone
from django.urls import reverse
from slugify import slugify

# Create your models here.
# 栏目数据类型
class ArticleColumn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_column')
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column

# 文章标签
class ArticleTag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag")
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag

# 文章数据类型
class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)#一篇文章可以多人点赞，一人可点赞多篇文章
    article_tag = models.ManyToManyField(ArticleTag, related_name='article_tag', blank=True)#可以为空

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),) #在数据库建立索引，提高读取速度

    def __str__(self):
        return self.title

    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs) #除了slug之外，其他元素都复用父类的save
    
    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug]) #获取某篇文章的URL，reverse函数实现了从name到path

    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug]) #跟上面函数类似，但是不同URL

# 评论数据类型
class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator.username, self.article)
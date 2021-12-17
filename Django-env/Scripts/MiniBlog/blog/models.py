from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 博客分类
class Category(models.Model):
	name = models.CharField(max_length=100, verbose_name='分类名')


# 博客标签
class Tag(models.Model):
	name = models.CharField(max_length=100, verbose_name='标签名')


# 博客文章
class Post(models.Model):
	# 文章标题
	title = models.CharField(max_length=70, verbose_name='文章标题')
	# 文章正文
	body = models.TextField(verbose_name='文章正文')
	# 文章创建时间
	created_time = models.DateTimeField(verbose_name='创建时间')
	# 文章修改时间
	modified_time = models.DateTimeField(verbose_name='修改时间')
	# 文章摘要 blank = True表示允许为空
	excerpt = models.CharField(max_length=200, blank=True)
	# 文章分类 on_delete = models.CASCADE 参数是关联删除，一对多
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	# 文章标签 多对多 一个文章可以有多个标签，一个标签也可以对应着多篇文章
	tags = models.ManyToManyField(Tag, blank=True)
	# 作者 一对多 一个作者可以写很多文章
	author = models.ForeignKey(User, on_delete=models.CASCADE)


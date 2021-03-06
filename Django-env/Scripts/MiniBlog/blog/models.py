from django.db import models
# Django后台管理系统的用户，不是自己定义的
from django.contrib.auth.models import User
# 为创建博客时自动填充时间调用模块
from django.utils import timezone
# 管理路由
from django.urls import reverse
# 自动生成摘要
import markdown
from django.utils.html import strip_tags

# 博客分类
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name



    def __str__(self):
        return self.name


# 博客标签
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签名')

    # 别名
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 博客文章
class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70, verbose_name='文章标题')
    # 正文
    body = models.TextField(verbose_name='文章正文')

    # 创建时间和修改时间 default自动填充当前时间
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modified_time = models.DateTimeField(verbose_name='修改时间')

    # 文章摘要 blank=True 允许为空
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要')

    # 分类 on_delete=models.CASCADE 参数是关联删除 一对多
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')

    # 标签 多对多，一个文章可以有多个标签，
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    # 作者 一对多，一个作者可以写很多文章，
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    # 重写save函数是为了，每次进行修改时把修改文章时间改为当前时间。
    # 增加自动添加摘要
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        if self.excerpt is None:
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    # 管理url记得导入reverse 第一个参数告诉Django找到blog下detail
    # 第二个参数把路由里的<int:pk> 替换为pk，例如/posts/2/
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 使用别名是为了在后台显示中文
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # 对文章进行排序，后插入的文章显示在最上面
        ordering = ['-created_time']

    def __str__(self):
        return self.title
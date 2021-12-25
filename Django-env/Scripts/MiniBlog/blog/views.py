# 导入模型中的Post使用object查询
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Post
import markdown
import re


def index(request):
	# 使用模板操作数据库，取到所有数据，然后使用order_by按插入时间排序。'后插入的显示在前面'
	post_list = Post.objects.all().order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})


# 博客详情页，导入系统的404页面，如果文章存在就显示，不存在就返回404页面
def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	# 用markdown解析文章
	md = markdown.Markdown(extensions=[
		'markdown.extensions.extra',
		'markdown.extensions.codehilite',
		# 'markdown.extensions.toc',
		# 美化锚点
		TocExtension(slugify=slugify)
	])

	post.body = md.convert(post.body)
	m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
	post.toc = m.group(1) if m is not None else ''
	return render(request, 'blog/detail.html', context={'post': post})

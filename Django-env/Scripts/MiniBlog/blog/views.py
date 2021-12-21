# blog\views.py

# 导入模型中的Post使用object查询
from django.shortcuts import render

from .models import Post

def index(request):

    # 使用模板操作数据库，取到所有数据，然后使用order_by按插入时间排序。'后插入的显示在前面'
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Blog,Category
from django.core.paginator import Paginator ,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your viewfrom django.http import Http404
from .forms import CommentForm


def get_blogs(request):
    all_blogs=Blog.objects.all().order_by('-created')
    blog_paginator=Paginator(all_blogs,8)#show 8 blogs per page
   
    page=request.GET.get('page')
    try:
        blogs=blog_paginator.page(page)
    except PageNotAnInteger:
        blogs=blog_paginator.page(1)
    except EmptyPage:
        blogs=blog_paginator(blog_paginator.num_pages)

    ctx = {
    'blogs': blogs,
    'categories':Category.objects.all(),

    }
    return render(request, 'blog-list.html', ctx)
    
# @ensure_csrf_cookie
def get_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404

    ctx ={
            'blog': blog,
            'categories':Category.objects.all(),
            }
    return render(request, 'blog-detail-new.html', ctx)
    
    
def get_category(request, category_id):
    try:
        cat=Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise Http404
    cat_blogset=cat.blog_set.all().order_by('-created')
    blog_paginator=Paginator(cat_blogset,8)#show 8 blogs per page
  
    page=request.GET.get('page')
    try:
        blogs=blog_paginator.page(page)
    except PageNotAnInteger:
        blogs=blog_paginator.page(1)
    except EmptyPage:
        blogs=blog_paginator(blog_paginator.num_pages)
    ctx = {
    'blogs': blogs,
    'categories':Category.objects.all(),
    }
    return render(request, 'blog-list.html', ctx)
    

def add_comment(request,blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404
    if request.is_ajax() and request.method == 'POST':
    #那就要把接收到的内容，放入数据库，同时添加到网页显示
        name=request.POST.get("name")
        email=request.POST.get("email")
        content=request.POST.get("content")
        data={
            "name":name,
            "email":email,
            "content":content,
            "blog":blog}
        Comment.objects.create(**data)
        return_data={
            "name":name,
            "content":content}
    return JsonResponse(return_data)
        



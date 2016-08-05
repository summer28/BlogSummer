from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Blog,Category,Comment
from django.core.paginator import Paginator ,EmptyPage,PageNotAnInteger

# Create your viewfrom django.http import Http404
from .forms import CommentForm


def get_blogs(request):
    all_blogs=Blog.objects.all().order_by('-created')
    blog_paginator=Paginator(all_blogs,3)#show 8 blogs per page
    page_num=blog_paginator.num_pages;
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
    "page_num":page_num,
    }
    return render(request, 'blog-list-new.html', ctx)

def get_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404

    if request.method == 'GET':
            form = CommentForm()
    else:
            form = CommentForm(request.POST)
    if form.is_valid():
             cleaned_data = form.cleaned_data 
             # django use cleaned_data to get the content of the form 
             # add  a blog key to the dictionary
             cleaned_data['blog'] = blog
             # use the dictionary to create a  Comment object 
             Comment.objects.create(**cleaned_data)

    ctx ={
            'blog': blog,
            'categories':Category.objects.all(),
            'comments': blog.comment_set.all().order_by('-created'),
            'form': form,


            }
    return render(request, 'blog-detail.html', ctx)
    
    
def get_category(request, category_id):
    try:
        cat=Category.objects.get(category_id)
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
    return render(request, 'blog-list-new.html', ctx)
    

def add_comment(request,blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404
    if request.is_ajax() and request.method == 'POST':
    #那就要把接收到的内容，放入数据库，同时添加到网页显示
        data={
            "name":request.POST.get("name"),
            "email":request.POST.get("email"),
            "content":request.POST.get("content"),
            "blog":blog,}
        Comment.objects.create(**data)
    return JsonResponse(data)
        



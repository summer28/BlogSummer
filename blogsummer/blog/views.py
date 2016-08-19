from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Blog,Category
from django.core.paginator import Paginator ,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.http import Http404
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
    categories=Category.objects.all()
    # categories_dic={}
    # for category in categories:
    #     c_blog=category.blog_set.all()
    #     c_blog_num=len(c_blog)
    #     categories_dic[category]=c_blog_num
    # #print( categories_dic)
    ctx ={
            'blog': blog,
            'categories':categories,
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
    

def blog_search(request):
    try:
        key=request.POST.get('blog_search')
        if not key:
            print("key null ")
            return index(request)
        try:
            blogs_set = Blog.objects.filter(title__contains=key).order_by('-created')

        except Exception:
            print("blog fail ")
            raise Http404("搜索文档失败")
        blog_paginator=Paginator(blogs_set,8)#show 8 blogs per page

        page=request.POST.get('page')
        try:
            blogs=blog_paginator.page(page)
        except PageNotAnInteger:
            blogs=blog_paginator.page(1)
        except EmptyPage:
            blogs=blog_paginator(blog_paginator.num_pages)
        print("page ok ")
        ctx = {
        'blogs': blogs,
        'categories':Category.objects.all(),
        }
        
    except Exception:
        raise Http404
    return render(request, 'blog-list.html', ctx)

def email_test(request):
    from django.core.mail import send_mail #导入django发送邮件模块
    send_mail(
        'blog',
        'email.',
        'blogemail666@163.com',
        ['13770512913@163.com'],
        fail_silently=False,
    )
    print("send ok")
    # import smtplib
    # from email.mime.text import MIMEText
    # from email.header import Header

    # # 第三方 SMTP 服务
    # mail_host="smtp.163.com"  #设置服务器
    # mail_user="13770512913@163.com"    #用户名
    # mail_pass="2wsx3edc"   #口令 


    # sender = '13770512913@163.com'
    # receivers = ['13770512913@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    # message['From'] = Header("菜鸟教程", 'utf-8')
    # message['To'] =  Header("测试", 'utf-8')

    # subject = 'Python SMTP 邮件测试'
    # message['Subject'] = Header(subject, 'utf-8')
   

    # try:
    #     smtpObj = smtplib.SMTP() 
    #     smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    #     print("coonect ok")
    #     smtpObj.login(mail_user,mail_pass)
    #     print("login ok")
    #     smtpObj.sendmail(sender, receivers, message.as_string())
    #     print ("邮件发送成功")
    # except smtplib.SMTPException:
    #     print ("Error: 无法发送邮件")
    
    try:
        blog = Blog.objects.get(id=9)
    except Blog.DoesNotExist:
        raise Http404

    ctx ={
            'blog': blog,
            'categories':Category.objects.all(),
            }
    return render(request, 'blog-list.html',ctx)

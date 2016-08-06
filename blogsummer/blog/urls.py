from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.get_blogs, name='blog_get_blogs'),
	url(r'^(?P<blog_id>\d+)/$', views.get_detail, name='blog_get_detail'),
	url(r'^cat/(?P<category_id>\d+)/$', views.get_category, name='blog_get_category'),
	url(r'^(?P<blog_id>\d+)/comment/$',views.add_comment, name='comment'),
]

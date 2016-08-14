from django.contrib import admin
from .models import Category, Tag, Blog
class BlogAdmin(admin.ModelAdmin):
	fields=['title','content','category']
	list_display=('title','created','author')
admin.site.register(Blog,BlogAdmin)
admin.site.register([Category,Tag])


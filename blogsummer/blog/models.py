from django.db import models

# Create your models here.
from django.db import models
 

class Category(models.Model):
    name = models.CharField('名称', max_length=16)
    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField('名称', max_length=16)
    def __str__(self):
        return self.name



class Blog(models.Model):
    title = models.CharField('标题', max_length=32)
    author = models.CharField('作者', max_length=16)
    content = models.TextField('正文')
    created = models.DateTimeField('发布时间', auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name='分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    # comment_set=models.ForeignKey(Comment,verbose_name='Comment') bidirectual relationship,don't need
    def __str__(self):
        return self.title



class Comment(models.Model):
    blog = models.ForeignKey(Blog, verbose_name='博客')
    name = models.CharField('称呼', max_length=16)
    email = models.EmailField('邮箱')
    content = models.CharField('内容', max_length=140)
    created = models.DateTimeField('发布时间', auto_now_add=True)
    
class Replay(models.Model):
    replay_user=models.CharField('称呼', max_length=16)
    replay_date=models.DateTimeField('发布时间', auto_now_add=True)
    content=models.TextField('正文')
    comment=models.ForeignKey(Comment, verbose_name='评论')


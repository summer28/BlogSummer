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


from ckeditor_uploader.fields import RichTextUploadingField
#from ckeditor.fields import RichTextField
class Blog(models.Model):
    title = models.CharField(verbose_name='Title',max_length=32)
    author = models.CharField(verbose_name='Author', max_length=16)
    #content = RichTextField()
    content=RichTextUploadingField('Content')
    created = models.DateTimeField(verbose_name='Pub_Date', auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name='Category')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
    # comment_set=models.ForeignKey(Comment,verbose_name='Comment') bidirectual relationship,don't need
    def __str__(self):
        return self.title







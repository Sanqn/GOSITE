from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class Hero(models.Model):
    title = models.CharField(max_length=250, verbose_name='Header')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to="photo/%Y/%m/%d/", blank=True, verbose_name='Picture')
    created_at = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Hero'
        verbose_name_plural = 'Hero'
        ordering = ['created_at', 'title']


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

# c = Category.objects.get(pk=1)
# c.hero_set.all() get all hero by category
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

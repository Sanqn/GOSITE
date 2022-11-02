from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'h1', 'url', 'description', 'content', 'created_at', 'is_published']
    list_display_links = ['id', 'h1']
    prepopulated_fields = {'url': ('title',)}


admin.site.register(Post, PostAdmin)




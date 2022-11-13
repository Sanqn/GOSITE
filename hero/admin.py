from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Hero, Category


class HeroAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'get_html_url', 'category', 'is_published']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    list_editable = ['is_published']
    list_filter = ['is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    fields = ['title', 'slug', 'image', 'get_html_url', 'category', 'is_published', 'created_at', 'time_update']
    readonly_fields = ['get_html_url', 'created_at', 'time_update']

    def get_html_url(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
    get_html_url.short_description = 'Picture'


admin.site.register(Hero, HeroAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)

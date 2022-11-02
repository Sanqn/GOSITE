from django.contrib import admin

from .models import Hero, Category


class HeroAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'image', 'created_at', 'time_update', 'category', 'is_published']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    list_editable = ['is_published']
    list_filter = ['is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Hero, HeroAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)

from django.core.cache import cache
from django.db.models import Count

from .models import Category

menu = [
    {'title': 'About', 'url': 'about'},
    {'title': 'Add article', 'url': 'article'},
    {'title': 'Contact me', 'url': 'contact'},
]


class DataMixin:
    paginate_by = 5

    def get_user_context(self, *args, **kwargs):
        #  Собираем context, изначально получаем в kwargs {'title': 'Main menu'}
        #  После добавляем в context menu и категории и возвращаем во view
        context = kwargs
        cats = cache.get('category')
        if not cats:
            cats = Category.objects.annotate(Count('hero'))
            cache.set('category', cats, 60)
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

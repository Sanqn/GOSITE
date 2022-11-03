from .models import Category

menu = [
    {'title': 'About', 'url': 'about'},
    {'title': 'Add article', 'url': 'article'},
    {'title': 'Contact me', 'url': 'contact'},
    {'title': 'Login', 'url': 'login'},
]


class DataMixin:
    def get_user_context(self, *args, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['menu'] = menu
        print('context under menu', context)
        context['cats'] = cats
        print('utils====================', context)
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

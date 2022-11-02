from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddArticleForm
from .models import Hero, Category

menu = [
    {'title': 'About', 'url': 'about'},
    {'title': 'Add article', 'url': 'article'},
    {'title': 'Contact me', 'url': 'contact'},
    {'title': 'Login', 'url': 'login'},
]


class HomeViewList(ListView):
    model = Hero
    template_name = 'hero/index.html'
    context_object_name = 'persons'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Main page'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Hero.objects.filter(is_published=True)


# class HomeView(View):
#     def get(self, request, *args, **kwargs):
#         persons = Hero.objects.all()
#         # cat = Category.objects.all() # заменили cat на пользовательский тэг templatetags/hero_tags.py
#         return render(request, 'hero/index.html', context={
#             'menu': menu,
#             # 'cat': cat,
#             'persons': persons,
#             'title': 'Main page',
#             'cat_selected': 0
#         })

class PostDetailView(DetailView):
    model = Hero
    template_name = 'hero/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'person'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['menu'] = menu
        context['title'] = f'Category {context["person"]}'
        return context


# class PostView(View):
#     def get(self, request, post_slug, *args, **kwargs):
#         person = get_object_or_404(Hero, slug=post_slug)
#         # cat = Category.objects.all()
#         return render(request, 'hero/post.html', context={
#             'menu': menu,
#             # 'cat': cat,
#             'person': person,
#             'title': 'Main page',
#             'cat_selected': person.category_id
#
#         })


class ShowCatViewList(ListView):
    model = Hero
    template_name = 'hero/index.html'
    context_object_name = 'persons'
    allow_empty = False

    def get_queryset(self):
        print(self.kwargs)  # {'cat_slug': 'fire-resistant'}
        return Hero.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = f'Category {context["persons"][0].category}'
        context['cat_selected'] = context['persons'][0].category_id
        return context
        # print('1111111', context) 1111111 {'paginator': None, 'page_obj': None, 'is_paginated': False,
        # 'object_list': <QuerySet [<Hero: Ironman>, <Hero: Superman>]>,
        # 'persons': <QuerySet [<Hero: Ironman>, <Hero: Superman>]>,
        # 'view': <hero.views.ShowCatViewList object at 0x0000023B4E28D1E0>,
        # 'menu': [{'title': 'About', 'url': 'about'}, {'title': 'Add article', 'url': 'article'},
        #          {'title': 'Contact me', 'url': 'contact'}, {'title': 'Login', 'url': 'login'}]}
        # print('22222222', context['persons'][0].category_id) # 1
        # print('3333', context['persons'][0].category)  # fly


# class ShowCatView(View):
#     def get(self, request, cat_slug, *args, **kwargs):
#         cats_slug = Category.objects.get(slug=cat_slug)
#         persons = Hero.objects.filter(category__slug=cat_slug)
#         # persons = Hero.objects.filter(category_id=cats_slug.id)
#         # cat = Category.objects.all() # заменили cat на пользовательский тэг templatetags/hero_tags.py
#         return render(request, 'hero/index.html', context={
#             'menu': menu,
#             # 'cat': cat,
#             'persons': persons,
#             'title': 'Main page',
#             'cat_selected': cats_slug.id
#         })


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('About')


class AddArticleCreateView(CreateView):
    form_class = AddArticleForm
    template_name = 'hero/addarticle.html'
    success_url = reverse_lazy('hero')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Add Article'
        return context


# class AddArticleView(View):
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             form = AddArticleForm()
#             return render(request, 'hero/addarticle.html', context={
#                 'forms': form,
#                 'menu': menu,
#                 'title': 'Add Article',
#             })
#
#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             form = AddArticleForm(request.POST, request.FILES)
#             if form.is_valid():
#                 ## if we use ModelForm
#                 form.save()
#                 ## if we use Form
#                 # try:
#                 #     Hero.objects.create(**form.cleaned_data)
#                 #     return redirect('hero')
#                 # except Exception as e:
#                 #     form.add_error(None, f'Error article {e}')
#         else:
#             form = AddArticleForm()
#         return render(request, 'hero/addarticle.html', context={
#             'form': form,
#             'menu': menu,
#             'title': 'Add Article',
#         })

# def new_add(request, *args, **kwargs):
#     if request.method == 'POST':
#         form = AddArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = AddArticleForm()
#     return render(request, 'hero/addarticle.html', context={
#         'form': form,
#         'menu': menu,
#         'title': 'Add Article',
#     })

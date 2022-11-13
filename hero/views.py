from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddArticleForm, SignUpForm
from .models import Hero, Category
from .utils import menu, DataMixin


class HomeViewList(DataMixin, ListView):
    # paginate_by = 1  # post this paginator in utils DataMixin
    model = Hero
    template_name = 'hero/index.html'
    context_object_name = 'persons'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # print('+++++++', list(context.items()))
        # +++++++ [('paginator', None), ('page_obj', None), ('is_paginated', False), ('object_list',
        # < QuerySet[< Hero: The Thing >, < Hero: Human Torch >, < Hero: Superman >, < Hero: Falcon >] >),
        #  ('persons', < QuerySet[< Hero: The Thing >, < Hero: Human Torch >, < Hero: Superman >, < Hero: Falcon >] >),
        #  ('view', < hero.views.HomeViewList object at 0x0000023C57CDF8E0 >)]
        con_def = self.get_user_context(title='Main menu')
        # print('=============', list(con_def.items()))
        # [('title', 'Main menu'), ('menu',
        # [{'title': 'About', 'url': 'about'}, {'title': 'Add article', 'url': 'article'},
        # {'title': 'Contact me', 'url': 'contact'}, {'title': 'Login', 'url': 'login'}]),
        # ('cats', < QuerySet[< Category: fly >, < Category: fire resistant >, < Category: fly and fire resistant >] >),
        # ('cat_selected', 0)]

        # return dict(list(context.items()) + list(con_def.items()))
        return context | con_def
        # context['menu'] = menu
        # context['title'] = 'Main page'
        # context['cat_selected'] = 0
        # return context

    def get_queryset(self):
        return Hero.objects.filter(is_published=True).select_related('category')


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

class PostDetailView(DataMixin, DetailView):
    model = Hero
    template_name = 'hero/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'person'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_menu = self.get_user_context(title=context["person"])
        return dict(list(context.items()) + list(cat_menu.items()))
        # print(context)
        # context['menu'] = menu
        # context['title'] = f'Category {context["person"]}'
        # return context


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


class ShowCatViewList(DataMixin, ListView):
    # paginate_by = 1  # post this paginator in utils DataMixin
    model = Hero
    template_name = 'hero/index.html'
    context_object_name = 'persons'
    allow_empty = False

    def get_queryset(self):
        print(self.kwargs)  # {'cat_slug': 'fire-resistant'}
        return Hero.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        cat_menu = self.get_user_context(title=f'Category {c.name}',
                                         cat_selected=c.pk)

        return dict(list(context.items()) + list(cat_menu.items()))
        # context['menu'] = menu
        # context['title'] = f'Category {context["persons"][0].category}'
        # context['cat_selected'] = context['persons'][0].category_id
        # return context
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
        all_hero = Hero.objects.all()
        paginator = Paginator(all_hero, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'hero/about.html', context={'page_obj': page_obj, 'menu': menu})


class AddArticleCreateView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'hero/addarticle.html'
    success_url = reverse_lazy('hero')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_menu = self.get_user_context(title='Add Article')
        return dict(list(context.items()) + list(cat_menu.items()))
        # context['menu'] = menu
        # context['title'] = 'Add Article'
        # return context


class SignUpView(DataMixin, CreateView):
    form_class = SignUpForm
    template_name = 'hero/signup1.html'
    success_url = reverse_lazy('signin')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_menu = self.get_user_context(title='SignUp')
        return context | cat_menu

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('hero')


class SignInView(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'hero/signin.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_menu = self.get_user_context(title='SignIn')
        return context | cat_menu

    def get_success_url(self):
        return reverse_lazy('hero')


def logout_user(request):
    logout(request)
    return redirect('hero')

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

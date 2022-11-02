from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Post
from .forms import SignUpForm, SignInForm
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth import authenticate


class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/index.html', context={
            'page_obj': page_obj
        })


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        return render(request, 'blog/post_detail.html', context={
            'post': post
        })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'blog/signup.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)  # <SignUpForm bound=True, valid=True, fields=(username;password;repassword)>
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()  # user: Al
            if user is not None:
                login(request, user)
                return_name_url = reverse('signup_access')
                return HttpResponseRedirect(return_name_url)
        return render(request, 'blog/signup.html', context={
            'form': form
        })


class SignUpAccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/access_signup.html')


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'blog/signin.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        print(request.POST)  # <QueryDict: {'csrfmiddlewaretoken':
        # ['wuLP7J02CTDsK5ufdmdvhmb4ZeuX3wM8DlDVtowDKIqVTY4ImaVuPIWh47V2Zl5t'],
        # 'username': ['admin'], 'password': ['admin']}>
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/signin.html', context={
            'form': form,
        })


class TeNo(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.get(id=2)
        descr = posts.description
        return HttpResponse(descr)


def user(request):  # http://127.0.0.1:8000/user?name=Tom&age=22
    print(request.GET)
    age = request.GET.get('age', 0)
    name = request.GET.get('name', 'Undefined')
    # return redirect('http://127.0.0.1:8000/')
    return HttpResponse(f'Your name is {name} and age {age}')


# -------------------------------- reverse ----------------------------------------
dict_li = {
    'li_0': 'nj cegth gtje ntcn lz  dct', 'bo_1': 'fke;fke fke;'
}


def go_user(request, some_name: str):
    print(some_name)
    name = dict_li.get(some_name)
    return HttpResponse(name)


def go_user_number(request, some_name: int):
    name = list(dict_li)
    print(name)
    name = name[some_name]
    print(name)
    return_name_url = reverse('gouser_name', args=[name])
    return HttpResponseRedirect(return_name_url)



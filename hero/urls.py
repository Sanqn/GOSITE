from django.urls import path, include
from .views import PostDetailView, ShowCatViewList, AboutView, AddArticleCreateView, HomeViewList, SignUpView, \
    SignInView, logout_user, ContactView
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('hero/', cache_page(60)(HomeViewList.as_view()), name='hero'),
    path('hero/', HomeViewList.as_view(), name='hero'),
    path('hero/about/', AboutView.as_view(), name='about'),
    path('hero/article/', AddArticleCreateView.as_view(), name='article'),
    path('hero/contact/', ContactView.as_view(), name='contact'),
    path('hero/signup/', SignUpView.as_view(), name='signup1'),
    path('hero/signin/', SignInView.as_view(), name='signin'),
    path('hero/logout/', logout_user, name='logout'),
    path('hero/category/<slug:cat_slug>/', ShowCatViewList.as_view(), name='category'),
    path('hero/<slug:post_slug>/', PostDetailView.as_view(), name='post'),
]

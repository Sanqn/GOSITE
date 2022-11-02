from django.urls import path, include
from .views import PostDetailView, ShowCatViewList, AboutView, AddArticleCreateView, HomeViewList


urlpatterns = [
    path('hero/', HomeViewList.as_view(), name='hero'),
    path('hero/about/', AboutView.as_view(), name='about'),
    path('hero/article/', AddArticleCreateView.as_view(), name='article'),
    path('hero/contact/', HomeViewList.as_view(), name='contact'),
    path('hero/login/', HomeViewList.as_view(), name='login'),
    path('hero/category/<slug:cat_slug>/', ShowCatViewList.as_view(), name='category'),
    path('hero/<slug:post_slug>/', PostDetailView.as_view(), name='post'),
]

from django.urls import path, include
from .views import MainView, TeNo, PostDetail, SignUpView, SignUpAccessView, SignInView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import views

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('blog/<slug>/', PostDetail.as_view(), name='postdetail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout', ),
    path('signup_access/', SignUpAccessView.as_view(), name='signup_access'),
    # ---------------------------------- Test pages ----------------------------------------------
    path('teno/', TeNo.as_view(), name='teno'),
    path('user/', views.user, name='user'),
    path('<int:some_name>/', views.go_user_number),
    path('<str:some_name>/', views.go_user, name='gouser_name')
]

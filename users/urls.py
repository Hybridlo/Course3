from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('user/<int:id>/', views.user_view, name='user'),
    path('reactivation/', views.reactivation, name='reactivation'),
    path('forgot/', views.forgot_password, name='forgot'),
    re_path(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.pass_reset, name='pass_reset'),
    path('staff_signup/', views.staff_signup, name='staff_signup'),
    path('create_staff_token/', views.create_staff_token, name='create_staff_token')
]
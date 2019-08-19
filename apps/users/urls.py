"""eduproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path
from apps.users import views
app_name = 'users'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    #path('user_login/', views.user_login, name='user_login'),
    path('user_login/', views.LoginView.as_view(), name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    re_path(r'^user_active/(\w+)/$', views.user_active, name='user_active'),
    path('user_forget/', views.user_forget, name='user_forget'),
    re_path(r'^user_reset/(\w+)/$', views.user_reset, name='user_reset'),
    path('user_info/', views.user_info, name='user_info'),
    path('user_message/', views.user_message, name='user_message'),
    #消息已阅读
    path('user_message_hasRead/', views.user_message_hasRead, name='user_message_hasRead'),
    path('user_course/', views.user_course, name='user_course'),
    path('user_fav_course/', views.user_fav_course, name='user_fav_course'),
    path('user_fav_teacher/', views.user_fav_teacher, name='user_fav_teacher'),
    path('user_fav_org/', views.user_fav_org, name='user_fav_org'),
    #删除用户收藏
    path('user_fav_del/', views.user_fav_del, name='user_fav_del'),
    path('user_change_image/', views.user_change_image, name='user_change_image'),
    path('user_change_info/', views.user_change_info, name='user_change_info'),
    path('user_change_email/', views.user_change_email, name='user_change_email'),
    path('user_reset_email/', views.user_reset_email, name='user_reset_email'),
]

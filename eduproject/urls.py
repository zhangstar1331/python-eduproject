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
from django.contrib import admin
import xadmin
from django.urls import path,include,re_path
from django.views.static import serve
from eduproject.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('captcha',include('captcha.urls')),
    path('users/', include('apps.users.urls',namespace='users')),
    path('operations/', include('apps.operations.urls')),
    path('orgs/', include('apps.orgs.urls',namespace='orgs')),
    path('courses/', include('apps.courses.urls')),
    # 处理 media 信息，用于图片获取
    re_path(r'^media/(?P<path>.*)', serve, {"document_root":MEDIA_ROOT}),
]
#全局404,500路由配置
handler404 = 'apps.users.views.page_not_found'
handler500 = 'apps.users.views.page_error'

"""learning_log URL Configuration

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
# Django2版本用path取代了之前的url,此外path不支持正则表达式，需要引用re_path
from django.urls import path, include
# from django.conf.urls import url, include

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'', include('learning_logs.urls', namespace='learning_logs')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    # 实参namespace区分开learning_logs的URL和项目其他的URL
    path('', include('learning_logs.urls', namespace='learning_logs')),
]

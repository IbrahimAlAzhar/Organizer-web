"""suorganizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include,url
from django.contrib import admin
from django.urls import path
from .views import redirect_root
from organizer.views import homepage,tag_detail
from organizer import urls as organizer_urls
from blog.views import PostList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',redirect_root), # in home url the url goes into automatically blog url for this  method
    # path('', include(organizer_urls)),
    path('organizer/',include('organizer.urls')),
    path('blog/',include('blog.urls')),
]

"""Autotransсript URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from login import views
from trash import views as v1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('welcome.urls')),
    path('user_window/', include('user_window.urls')),
    path('join/', include('join.urls')),
    path('create/', include('create.urls')),
    path('login/', include('login.urls')),
    path('registrate/', include('registrate.urls')),
    path('logout/', views.logoutUser, name='logout'),
    path('chat/', include('chat.urls')),
    path('trash/',include('trash.urls')),
    # path('trash/',v1.download, name ="script2"),
]

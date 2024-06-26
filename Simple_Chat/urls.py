"""
URL configuration for Simple_Chat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from chat.views import index, login_view, signup_view, logout_view, get_messages, users_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('chat/', index),
    path('login/', login_view),
    path('signup/', signup_view),
    path('logout/', logout_view),
    path('chat/get_messages/', get_messages),
    path('users/', users_view),
]

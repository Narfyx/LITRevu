"""
URL configuration for LITRevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from authentification import views as auth_view
from actions_users import views as actions_view
from .views import index

urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("", auth_view.connexion, name="connexion"),
    path("inscription", auth_view.inscription, name="inscription"),
    path("user_follow", actions_view.user_follow, name="user_follow"),
    path('deconnexion/', auth_view.deconnexion, name='deconnexion'),
    
]

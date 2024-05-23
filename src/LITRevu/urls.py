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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from actions_users import views as actions_view
from authentification import views as auth_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth_view.connexion, name="connexion"),
    path("inscription/", auth_view.inscription, name="inscription"),
    path("deconnexion/", auth_view.deconnexion, name="deconnexion"),
    path("search_user/", actions_view.search_user),
    path("follow/<str:username>/", actions_view.follow_user, name="follow_user"),
    path("unfollow/<str:username>/", actions_view.unfollow_user, name="unfollow_user"),
    path("flux", actions_view.flux, name="flux"),
    path("my_post", actions_view.my_post, name="my_post"),
    path("create_ticket", actions_view.create_ticket, name="create_ticket"),
    path(
        "create_ticket_and_review",
        actions_view.create_ticket_and_review,
        name="create_ticket_and_review",
    ),
    path("create_review", actions_view.create_review, name="create_review"),
    path(
        "create_review/<int:ticket_id>/",
        actions_view.create_review,
        name="create_review",
    ),
    path("follow/", actions_view.user_follow, name="user_follow"),
    path("edit_ticket/<int:ticket_id>/", actions_view.ticket_edit, name="ticket_edit"),
    path("edit_review/<int:review_id>/", actions_view.edit_review, name="edit_review"),
    path(
        "delete_review/<int:review_id>/",
        actions_view.delete_review,
        name="delete_review",
    ),
    path(
        "delete_ticket/<int:ticket_id>/",
        actions_view.delete_ticket,
        name="delete_ticket",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

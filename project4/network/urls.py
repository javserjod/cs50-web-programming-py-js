
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username_to_follow>", views.follow, name="follow"),
    path("unfollow/<str:username_to_unfollow>",
         views.unfollow, name="unfollow"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("delete_post", views.delete_post, name="delete_post"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("gamemode/music_video", views.music_video, name="music_video"),


]

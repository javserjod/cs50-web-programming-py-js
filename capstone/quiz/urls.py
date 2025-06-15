from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("game_configuration", views.game_configuration, name="game_configuration"),
    path("game_update/<int:game_id>", views.game_update, name="game_update"),
    path("skip_round/<int:game_id>", views.skip_round, name="skip_round"),

]

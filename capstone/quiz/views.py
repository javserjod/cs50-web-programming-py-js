from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from quiz.models import User

# Create your views here.


def home(request):
    if request.method == "GET":
        return render(request, "quiz/home.html")


def register(request):
    if request.method == "GET":
        return render(request, "quiz/register.html")

    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "quiz/register.html", {
                "message": "Passwords must match."
            })
        image_url = request.POST.get("image_url")
        if not image_url:
            image_url = "https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small_2x/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg"
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                profile_picture_url=image_url
            )
            user.save()
        except IntegrityError:
            return render(request, "quiz/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "quiz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "quiz/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


@login_required
def profile(request, username):
    if request.method == "GET":
        return render(request, "quiz/profile.html")


@login_required
def game_configuration(request):
    if request.method == "GET":
        return render(request, "quiz/game_configuration.html")
    elif request.method == "POST":
        game_mode = request.POST.get("game_mode")
        number_of_questions = request.POST.get("number_of_questions")
        print(f"Selected game mode: {game_mode}")


@login_required
def music_video(request):
    if request.method == "GET":
        return render(request, "quiz/gamemodes/music_video.html")
    elif request.method == "POST":
        pass

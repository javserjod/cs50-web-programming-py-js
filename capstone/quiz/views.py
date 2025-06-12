from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from quiz.models import User, Game
import requests
import re


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
        # create a new game instance
        user = request.user
        game_topic = request.POST.get("game_topic")
        game_mode = request.POST.get("game_mode")
        number_of_questions = int(request.POST.get("number_of_questions"))
        try:
            game = Game.objects.create(
                user=user,
                game_topic=game_topic,
                game_mode=game_mode,
                number_of_questions=number_of_questions
            )
            game.save()   # game created
            return HttpResponseRedirect(reverse("game_update", args=[game.id]))
        except IntegrityError:
            return render(request, "quiz/game_configuration.html", {
                "message": "Error creating game. Please try again."
            })


@login_required
def game_update(request, game_id):
    if request.method == "GET":
        game = get_object_or_404(Game, id=game_id, user=request.user)
        topic = game.game_topic

        if game.game_mode == "mix":
            pass
        elif game.game_mode == "cover_image":
            pass
        elif game.game_mode == "character_image":
            pass
        elif game.game_mode == "title":
            pass


def search_youtube(song_name, artist_name):
    """
    Search for a YouTube video using the song name and artist name.
    Scrapes the YouTube search results page to find the first video that matches the query and extracts the video ID.
    """
    query = f"{song_name} {artist_name}".replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)

    match = re.search(r'"videoId":"(.*?)"', response.text)
    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None


def search_dailymotion(song_name, artist_name):
    """
    Search for a YouTube video using the song name and artist name.
    Scrapes the YouTube search results page to find the first video that matches the query and extracts the video ID.
    """
    query = f"{song_name} {artist_name}"
    url = "https://api.dailymotion.com/videos"
    params = {
        "search": query,
        "fields": "id,title",
        "limit": 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["list"]:
            return data["list"][0]["id"]
    return None

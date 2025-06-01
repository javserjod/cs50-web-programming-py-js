from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Post, Comment


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        author = request.user
        content = request.POST["content"]
        post = Post.objects.create(author=author, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "network/index.html", {
            "posts": Post.objects.all().order_by("-date"),
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):
    if request.method == "POST":
        pass
    else:
        profile_user = get_object_or_404(User, username=username)
        profile_user_posts = Post.objects.filter(
            author=profile_user).order_by("-date")
        is_followed = profile_user.is_followed_by(request.user)
        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "profile_user_posts": profile_user_posts,
            "is_followed": is_followed,
        })


@login_required
def follow(request, username_to_follow):
    if request.method == "POST":
        user_to_follow = get_object_or_404(User, username=username_to_follow)
        request.user.following.add(user_to_follow)
        return HttpResponseRedirect(reverse("profile", args=[username_to_follow]))


@login_required
def unfollow(request, username_to_unfollow):
    if request.method == "POST":
        user_to_unfollow = get_object_or_404(
            User, username=username_to_unfollow)
        request.user.following.remove(user_to_unfollow)
        return HttpResponseRedirect(reverse("profile", args=[username_to_unfollow]))

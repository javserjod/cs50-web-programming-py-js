from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import User, Post, Comment

POSTS_PER_PAGE = 10


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        # Create post
        author = request.user
        content = request.POST["content"]
        post = Post.objects.create(author=author, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        # Display all posts
        all_posts = Post.objects.all().order_by("-date")
        paginator = Paginator(all_posts, POSTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            'page_obj': page_obj
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
        image_url = request.POST["image_url"]
        if not image_url:
            image_url = "https://t4.ftcdn.net/jpg/02/15/84/43/360_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg"
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, image_url=image_url)
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

        all_profile_user_posts = Post.objects.filter(
            author=profile_user).order_by("-date")
        paginator = Paginator(all_profile_user_posts, POSTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        is_followed = profile_user.is_followed_by(request.user)
        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "page_obj": page_obj,
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


@login_required
def following(request):
    if request.method == "POST":
        pass
    else:
        following_users = request.user.following.all()
        all_following_posts = Post.objects.filter(
            author__in=following_users).order_by("-date")

        paginator = Paginator(all_following_posts, POSTS_PER_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/following.html", {
            "page_obj": page_obj,
        })


@login_required
def edit_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, pk=data.get("post_id"))
            post.content = data.get("content")
            post.save()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=400)


@login_required
def delete_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, pk=data.get("post_id"))
            post.delete()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=400)


@login_required
def like_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, pk=data.get("post_id"))
            post.liked_by.add(request.user)
            post.save()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=400)


@login_required
def unlike_post(request):
    pass
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, pk=data.get("post_id"))
            post.liked_by.remove(request.user)
            post.save()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=400)

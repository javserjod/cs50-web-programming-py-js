from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from quiz.models import User, Game, Round
import requests
import random
import re
import numpy as np
import cv2
import base64


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
        try:
            game = Game.objects.create(
                user=request.user,
                topic=request.POST.get("game_topic"),
                mode=request.POST.get("game_mode"),
                genres=request.POST.getlist("game_genres"),
                n_questions=int(
                    request.POST.get("number_of_questions"))
            )

            for i in range(1, game.n_questions + 1):   # 1-based index
                # create a round for each question
                game.rounds.create(
                    number=i,
                    state="PENDING"
                )

            game.save()

            return HttpResponseRedirect(reverse("game_update", args=[game.id]))
        except IntegrityError:
            return render(request, "quiz/game_configuration.html", {
                "message": "Error creating game. Please try again."
            })


@login_required
def game_update(request, game_id):
    if request.method == "GET":
        game = get_object_or_404(Game, id=game_id, user=request.user)
        topic = game.topic
        genres = game.genres
        current_round = game.current_round()

        if game.mode == "mix":
            pass

        elif game.mode == "cover_image":
            if current_round.image_url:   # just reload the page
                return render(request, "quiz/gamemodes/guess_image.html", {
                    "game": game,
                    "rounds": range(1, game.n_questions + 1),
                    # "image_url": current_round.image_url,
                    "modified_image": current_round.modified_image
                })
            else:  # no image asigned for the round yet
                # asign a new modified image to the round
                image_url = get_cover_image(topic, genres)
                modified_image = image_random_modify(image_url)
                # save info for the current round
                current_round.image_url = image_url
                current_round.modified_image = modified_image
                current_round.save()
                return render(request, "quiz/gamemodes/guess_image.html", {
                    "game": game,
                    "rounds": range(1, game.n_questions + 1),
                    # "image_url": image_url,
                    "modified_image": modified_image
                })

        elif game.mode == "character_image":
            if current_round.image_url:   # just reload the page
                return render(request, "quiz/gamemodes/guess_image.html", {
                    "game": game,
                    "rounds": range(1, game.n_questions + 1),
                    # "image_url": current_round.image_url,
                    "modified_image": current_round.modified_image
                })
            else:  # no image asigned for the round yet
                # asign a new modified image to the round
                image_url = get_cover_image(topic, genres)
                modified_image = image_random_modify(image_url)
                # save info for the current round
                current_round.image_url = image_url
                current_round.modified_image = modified_image
                current_round.save()
                return render(request, "quiz/gamemodes/guess_image.html", {
                    "game": game,
                    "rounds": range(1, game.n_questions + 1),
                    # "image_url": image_url,
                    "modified_image": modified_image
                })

        elif game.mode == "title":
            pass


N_FETCHED_ELEMENTS = "50"  # number of media items to fetch from Anilist


def get_cover_image(topic, genres):
    genres_list = genres_to_list(genres)
    random_genre = random.choice(genres_list)
    url = 'https://graphql.anilist.co'
    query = '''
    query ($type: MediaType, $genre: [String]) {
        Page(perPage: 50) {
            media(type: $type, genre_in: $genre, sort: POPULARITY_DESC) {
                id
                title {
                    romaji
                }
                coverImage {
                    large
                }
            }
        }
    }
    '''
    variables = {
        "type": topic.upper(),
        "genre": random_genre
    }
    print("Fetching cover image for genre:", random_genre)
    response = requests.post(
        url, json={"query": query, "variables": variables})
    data = response.json()
    media_list = data["data"]["Page"]["media"]
    print("Random genre:", random_genre)

    if media_list:
        random_media = random.choice(media_list)   # Get a random media item
        # random media ordered by popularity. Difficulty could be leveraged with this.
        return random_media["coverImage"]["large"]
    return None


def get_character_image(topic, genres):
    genres_list = genres_to_list(genres)
    random_genre = random.choice(genres_list)

    url = "https://graphql.anilist.co"
    query = '''
    query ($type: MediaType, $genre: [String]) {
      Page(perPage: 50) {
        media(type: $type, genre_in: $genre, sort: POPULARITY_DESC) {
          characters(sort: ROLE) {
            nodes {
              name {
                full
              }
              image {
                large
              }
            }
          }
        }
      }
    }
    '''

    variables = {
        "type": topic.upper(),  # Should be "ANIME"
        "genre": random_genre
    }

    response = requests.post(
        url, json={"query": query, "variables": variables})
    data = response.json()

    media_list = data.get("data", {}).get("Page", {}).get("media", [])

    # valid characters with images
    candidates = []
    for media in media_list:
        characters = media.get("characters", {}).get("nodes", [])
        for character in characters:
            img = character.get("image", {}).get("large")
            if img:
                candidates.append(img)

    if candidates:
        return random.choice(candidates)

    return None


def image_random_modify(image_url):
    """
    Randomly modify an image from a URL.
    The modification can be either blurring or pixelating the image.
    Returns the modified image as a base64 string.
    """
    return pixelate_image_from_url(image_url)


def blur_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code != 200:
        return HttpResponse(status=404)

    image_data = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    # apply Gaussian blur to the image
    # bigger kernel size means more blur
    blurred = cv2.GaussianBlur(image, (51, 51), 0)

    success, buffer = cv2.imencode('.jpg', blurred)
    if not success:
        return None

    # convert the image to base64
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"


def pixelate_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code != 200:
        return HttpResponse(status=404)

    image_data = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    height, width = image.shape[:2]
    # desired "pixelated" size
    w, h = (16, 16)

    # resize image to "pixelated" size
    temp = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)

    # go back to original size
    pixelated = cv2.resize(temp, (width, height),
                           interpolation=cv2.INTER_NEAREST)

    success, buffer = cv2.imencode('.jpg', pixelated)
    if not success:
        return None

    # convert the image to base64
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"


def genres_to_list(genres):
    """
    Convert a string with comma-separated genres into a list.
    Genres is saved in model as a unique String inside a list, so we need to split it.
    Return a list of genres.
    """
    return [genre for genre in genres[0].split(",")]

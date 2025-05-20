from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import User, AuctionListing


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def listing(request, listing_id):
    if request.method == "GET":
        listing = AuctionListing.objects.get(pk=listing_id)
        return render(request, "auctions/listing.html", {"listing": listing})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    else:
        listing = AuctionListing(
            title=request.POST["title"],
            description=request.POST["description"],
            image_url=request.POST["image_url"],
            created_by=request.user,
            starting_bid=request.POST["starting_bid"],
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))


@login_required
# Show watchlist. Manage watchlist items.
def watchlist(request):
    if request.method == "GET":
        watchlisted_listings = request.user.watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "watchlisted_listings": watchlisted_listings
        })
    else:
        if request.POST["action"] == "add":
            new_watchlisted_listing = AuctionListing.objects.get(
                pk=request.POST["listing_id"])
            request.user.watchlist.add(new_watchlisted_listing)
        else:   # action: remove from watchlist
            listing = AuctionListing.objects.get(pk=request.POST["listing_id"])
            request.user.watchlist.remove(listing)

        return HttpResponseRedirect(reverse("listing", args=[request.POST["listing_id"]]))


@login_required
def bid(request):
    pass

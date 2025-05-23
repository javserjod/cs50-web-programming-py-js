from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db.models import Count


from .models import User, AuctionListing, Bid, Comment


def index(request):
    listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def closed_listings(request):
    listings = AuctionListing.objects.filter(is_active=False)
    return render(request, "auctions/closed_listings.html", {
        "listings": listings
    })


def listing(request, listing_id):
    if request.method == "GET":
        listing = get_object_or_404(AuctionListing, pk=listing_id)
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
            return redirect("index")
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
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    else:
        default_category = AuctionListing._meta.get_field(
            "category").get_default()   # to avoid hardcoding
        listing = AuctionListing(
            title=request.POST["title"],
            description=request.POST["description"],
            image_url=request.POST["image_url"],
            created_by=request.user,
            starting_bid=request.POST["starting_bid"],
            category=request.POST["category"].lower(
            ) or default_category.lower(),
        )
        listing.save()
        return redirect("index")


@login_required
# Show watchlist. Manage watchlist items. (HTML made to only watchlist other users' listings. Own listings reachable via user_listings)
def watchlist(request):
    if request.method == "GET":
        watchlisted_listings = request.user.watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "watchlisted_listings": watchlisted_listings
        })
    else:
        listing_id = request.POST["listing_id"]
        if request.POST["action"] == "add":
            new_watchlisted_listing = get_object_or_404(
                AuctionListing, pk=listing_id)
            request.user.watchlist.add(new_watchlisted_listing)
        else:   # action: remove from watchlist
            listing = get_object_or_404(
                AuctionListing, pk=listing_id)
            request.user.watchlist.remove(listing)

        return redirect("listing", listing_id)


@login_required
def bid(request):
    if request.method == "POST":
        listing = get_object_or_404(
            AuctionListing, pk=request.POST["listing_id"])

        bid_amount = request.POST["bid_amount"]

        if Decimal(bid_amount) > listing.starting_bid and Decimal(bid_amount) > listing.highest_bid():
            # create new bid
            new_bid = Bid.objects.create(
                user=request.user, listing=listing, amount=bid_amount)
            new_bid.save()

            messages.success(request, "Highest bid placed successfully.")
            return redirect("listing", listing.id)
        else:
            messages.warning(
                request, "Bid amount must be higher than the starting bid and the current highest bid.")
            return redirect("listing", listing.id)
    else:
        return redirect("index")


@login_required
def close_auction(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        listing.is_active = False
        listing.save()
        return redirect("index")
    else:
        return redirect("index")


@login_required
def remove_auction(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        listing.delete()
        return redirect("index")
    else:
        return redirect("index")


@login_required
def comment(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = get_object_or_404(AuctionListing, pk=listing_id)

        new_comment = Comment.objects.create(
            text=request.POST["comment_text"],
            user=request.user,
            listing=listing
        )
        new_comment.save()
        return redirect("listing", listing_id)
    else:
        return redirect("index")


def all_categories(request):
    if request.method == "GET":
        categories = (
            AuctionListing.objects.filter(is_active=True)
            .values('category')
            .annotate(total=Count('id'))
            .order_by('category')
        )
        return render(request, "auctions/all_categories.html", {
            # return list of dictionaries {'category': '...', 'total': ...}
            "categories": categories
        })
    else:
        return redirect("index")


def category_listings(request, category):
    if request.method == "GET":
        listings = AuctionListing.objects.filter(
            category=category, is_active=True)
        return render(request, "auctions/category_listings.html", {
            "listings": listings,
            "category": category
        })
    else:
        return redirect("index")


@login_required
def user_listings(request, username):
    if request.method == "GET":
        user_obj = get_object_or_404(User, username=username)
        listings = AuctionListing.objects.filter(created_by=user_obj)
        return render(request, "auctions/user_listings.html", {
            "creator_user": user_obj,
            "listings": listings
        })
    else:
        return redirect("index")

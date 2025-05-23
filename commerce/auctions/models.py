from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(
        "AuctionListing", blank=True, related_name="watchlisted_by", null=True)


class AuctionListing(models.Model):
    # creation information
    title = models.CharField(
        max_length=64, unique=True, null=False, blank=False)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_listings", null=False, blank=False)
    starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(
        max_length=64, blank=True, null=True, default="Uncategorized")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - by {self.created_by}"

    def highest_bid(self):
        highest = self.bids.order_by('-amount').first()
        return highest.amount if highest else self.starting_bid

    def current_bid_user(self):  # also the winner so far
        highest = self.bids.order_by('-amount').first()
        return highest.user if highest else None


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} by {self.user} on {self.listing.title}"


class Comment(models.Model):
    text = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.text} by {self.user} on {self.listing.title}"

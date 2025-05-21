from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_categories", views.all_categories, name="all_categories"),
    path("category/<str:category>",
         views.category_listings, name="category_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("user_listings/<str:username>",
         views.user_listings, name="user_listings"),
    path("bid", views.bid, name="bid"),
    path("close_auction", views.close_auction, name="close_auction"),
    path("remove_auction", views.remove_auction, name="remove_auction"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("comment", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

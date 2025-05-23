from django.contrib import admin

# Register your models here.
from .models import User, AuctionListing, Bid, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('watchlist',)


class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'starting_bid', 'is_active')
    list_filter = ('created_by__username',)
    search_fields = ('title', 'description', 'created_by__username')
    ordering = ('-is_active', 'id')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'amount')
    list_filter = ('listing',)
    search_fields = ('user__username', 'listing__title')
    ordering = ('listing', '-amount',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'text')
    list_filter = ('listing',)
    search_fields = ('user__username', 'listing__title')
    ordering = ('listing', '-id',)


admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)

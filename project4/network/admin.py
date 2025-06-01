from django.contrib import admin
from .models import User, Post, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',
                    'followers_count', 'following_count', 'posts_count')
    search_fields = ('username', 'email')
    filter_horizontal = ('followers', )


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'formatted_date', 'like_count')
    search_fields = ('author__username', 'content')
    list_filter = ('author', 'date')
    filter_horizontal = ('liked_by', )

    # Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

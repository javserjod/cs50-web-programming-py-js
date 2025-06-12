from django.contrib import admin

# Register your models here.
from quiz.models import User, Game


admin.site.register(User)
admin.site.register(Game)

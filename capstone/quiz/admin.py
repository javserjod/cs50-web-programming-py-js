from django.contrib import admin

# Register your models here.
from quiz.models import User, Game, Round


admin.site.register(User)
admin.site.register(Game)
admin.site.register(Round)

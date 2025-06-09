from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    profile_picture_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.username


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score} - {self.date_played}"

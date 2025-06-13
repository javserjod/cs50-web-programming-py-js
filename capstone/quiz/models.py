from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    profile_picture_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.username


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    topic = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    genres = models.JSONField(default=list)
    n_questions = models.IntegerField(default=10)

    def __str__(self):
        return f"Game #{self.id}, from {self.user.username}"

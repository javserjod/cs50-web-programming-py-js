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

    source = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    genres = models.JSONField(default=list)
    n_questions = models.IntegerField(default=10)

    def __str__(self):
        return f"Game #{self.id}, from {self.user.username}"

    def current_round(self):
        return self.rounds.filter(state=Round.PENDING).first()

    def is_finished(self):
        return not self.rounds.filter(state=Round.PENDING).exists()


class Round(models.Model):
    PENDING = 'PENDING'
    CORRECT = 'CORRECT'
    WRONG = 'WRONG'
    ROUND_STATES = [
        (PENDING, 'Pending'),
        (CORRECT, 'Correct'),
        (WRONG, 'Wrong'),
    ]
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='rounds')
    number = models.IntegerField()
    state = models.CharField(
        max_length=10, choices=ROUND_STATES, default='PENDING')

    db_entry_id = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    modified_image = models.TextField(blank=True, null=True)

    user_answer = models.CharField(max_length=200, blank=True, null=True)
    correct_answer = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Round {self.number} of Game #{self.game.id}"

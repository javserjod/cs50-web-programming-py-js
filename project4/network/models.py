from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='following', blank=True)

    image_url = models.URLField(
        default="https://t4.ftcdn.net/jpg/02/15/84/43/360_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg", blank=True)

    def __str__(self):
        return f"{self.username}"

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def posts_count(self):
        return self.posts.count()

    def is_followed_by(self, user):
        return self.followers.filter(id=user.id).exists()


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    date = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post {self.id} by {self.author.username} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

    def formatted_date(self):
        return self.date.strftime('%B %d, %Y, %H:%M %p')

    def like_count(self):
        return self.liked_by.count()


class Comment(Post):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author.username} on post {self.post.id} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

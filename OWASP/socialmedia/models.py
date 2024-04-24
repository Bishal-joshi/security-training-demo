from django.db import models
from authentication.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    likes = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.email}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.post}"

# gevox_posts models.py
from typing import Any
from django.db import models
from django.contrib.auth.models import User

class Sparks(models.Model):
    sparks = models.CharField(max_length=100)

    def __str__(self):
        return self.sparks


class PostModel(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    sparks = models.ManyToManyField(Sparks)
    likes = models.ManyToManyField(User, related_name='liked_posts')

    def __str__(self):
        return self.title


# comment model 
class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
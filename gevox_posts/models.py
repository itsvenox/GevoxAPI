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
    image_url = models.URLField(blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    sparks = models.ManyToManyField(Sparks)
    likes = models.ManyToManyField(User, related_name='liked_posts')
    # comments = models.ManyToManyField(CommentModel,)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.author.userprofile.reputation += 5
        # Calculate the number of new likes
        new_likes = self.likes.count() - self.__class__.objects.get(pk=self.pk).likes.count()

        # Increase user's reputation by 2 for each new like
        self.author.userprofile.reputation += 2 * new_likes
        self.author.userprofile.save()

        super().save(*args, **kwargs)


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
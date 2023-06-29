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

    def __str__(self):
        return self.title


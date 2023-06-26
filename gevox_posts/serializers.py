from rest_framework import serializers
from .models import PostModel

class PostSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PostModel
        fields = ['title', 'description', 'author', 'createdAt']


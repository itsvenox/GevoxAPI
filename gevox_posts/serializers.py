# serializer.py

from rest_framework import serializers
from .models import PostModel, Sparks

class PostSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(read_only=True)
    sparks = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'description', 'author', 'createdAt', 'sparks', 'likes_count']

    def get_likes_count(self, post):
        return post.likes.count()


class SparkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sparks
        fields = ['id', 'sparks']
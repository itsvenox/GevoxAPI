from rest_framework import serializers
from .models import PostModel

class PostSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(read_only=True)
    sparks = serializers.StringRelatedField(many=True)

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'description', 'author', 'createdAt', 'sparks']

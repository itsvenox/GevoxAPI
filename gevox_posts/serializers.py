# gevox_posts/serializers.py
from rest_framework import serializers
from .models import PostModel, Sparks, CommentModel
from gevox_authentication.serializers import UserProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    author_profile_pic = serializers.URLField(source='user.userprofile.profile_picture', read_only=True)
    author = serializers.CharField(source='user.userprofile.email', read_only=True)
    
    class Meta:
        model = CommentModel
        fields = '__all__'


class SparkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sparks
        fields = ['id', 'sparks']


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    sparks = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    author_profile = UserProfileSerializer(source='author.userprofile', read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    # liked_userIds = serializers.SerializerMethodField()

    class Meta:
        model = PostModel
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'author', 'created_at', 'sparks', 'likes_count', 'comments_count', 'author_profile']

    def get_likes_count(self, post):
        return post.likes.count()


    def get_comments_count(self, post):
        return CommentModel.objects.filter(post=post).count()
# gevox_authentication serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from gevox_posts.serializers import PostSerializer
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class profileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    posts = PostSerializer(many=True, read_only=True, source='user.postmodel_set')
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta(object):
        model = UserProfile
        fields = ['id', 'username', 'profile_picture', 'bio', 'posts', 'followers_count', 'following_count']

    def get_followers_count(self, user_profile):
        return user_profile.user.followers.count()

    def get_following_count(self, user_profile):
        return user_profile.user.following.count()
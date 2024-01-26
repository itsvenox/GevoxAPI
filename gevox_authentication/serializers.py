# gevox_authentication/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    joined_date = serializers.CharField(source='user.joined_date', read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_ids = serializers.SerializerMethodField()


    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'profile_picture', 'joined_date', 'bio', 'level','reputation', 'followers_count', 'following_count', 'followers_ids']

    def get_followers_count(self, user_profile):
        return user_profile.user.followers.count()

    def get_following_count(self, user_profile):
        return user_profile.user.following.count()

    def get_followers_ids(self, user_profile):
        return [follower.follower_id for follower in user_profile.user.followers.all()]

# public urls
from django.urls import path

from . import views

urlpatterns = [
    path('profile/<int:pk>/', views.userProfileAPI),
    path('follow/<int:id>/', views.followUserAPI, name='follow-user'),
    path('unfollow/<int:id>/', views.unfollowUserAPI, name='unfollow-user'),
]
# public urls
from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/profile/', views.userProfileAPI),
    path('<int:id>/follow/', views.followUserAPI, name='follow-user'),
    path('<int:id>/unfollow/', views.unfollowUserAPI, name='unfollow-user'),
]
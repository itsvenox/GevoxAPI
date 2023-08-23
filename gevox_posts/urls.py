# gevox_aposts urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('create-post/', views.createPostAPI),
    path('delete-post/<int:pk>/', views.deletePostAPI),
    path('get-post/<int:pk>/', views.getPostAPI),
    path('get-posts/', views.getAllPostsAPI),
    path('like/<int:pk>/', views.likePostAPI, name='like_post'),
    path('new-spark/', views.newSparkAPI)
]
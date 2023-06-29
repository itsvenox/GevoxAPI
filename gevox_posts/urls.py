from django.urls import path

from . import views

urlpatterns = [
    path('create-post/', views.createPostAPI),
    path('delete-post/<int:pk>/', views.deletePostAPI),
    path('get-post/<int:pk>/', views.getPostAPI),
    path('get-posts/', views.getAllPostsAPI)
]
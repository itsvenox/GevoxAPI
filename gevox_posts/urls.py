# gevox_aposts urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('create-post/', views.createPostAPI),
    path('delete-post/<int:post_id>/', views.deletePostAPI),
    path('get-post/<int:post_id>/', views.getPostAPI),
    path('get-posts/', views.getAllPostsAPI),
    path('like/<int:post_id>/', views.likePostAPI, name='like_post'),
    path('comment/add/<int:post_id>/', views.addCommentAPI, name='add-comment'),
    path('comment/delete/<int:comment_id>/', views.deleteCommentAPI, name='delete-comment'),
    path('comments/<int:post_id>/', views.getCommentsAPI),
    path('new-spark/', views.newSparkAPI)
]


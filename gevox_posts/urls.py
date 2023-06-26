from django.urls import path

from . import views

urlpatterns = [
    path('create-post/', views.createPostAPI),
    path('delete-post/<int:pk>/', views.deletePostAPI),
    # path('edit/<int:pk>/', views.editPostAPI),
]
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginAPI),
    path('signup/', views.signupAPI),
    path('delete-user/', views.deleteUserAPI),
    path("token-authenticated/", views.tokenAuthenticatedAPI)
]
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginAPI),
    path('signup/', views.signupAPI),
    path('logout/', views.logoutAPI),
    path('ban-user/', views.banUserAPI),
]
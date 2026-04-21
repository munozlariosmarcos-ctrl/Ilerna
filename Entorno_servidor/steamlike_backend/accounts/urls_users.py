from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.me, name="users-me"),
    path("me/password/", views.change_password, name="users-change-password"),  
]
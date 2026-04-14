from django.urls import path
from .view import register_view

urlpatterns = [
    path("register/", register_view, name="register"),
]
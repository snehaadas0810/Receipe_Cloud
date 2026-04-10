from django.urls import path
from .views import create_post, delete_post
from . import views

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path('create-post/', views.create_post, name='create_post'),
]
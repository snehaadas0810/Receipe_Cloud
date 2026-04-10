from django.urls import path
from .views import create_post, delete_post
from . import views

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    path('create-post/', views.create_post, name='create_post'),
    path('create/', views.create_post, name='create_post'),
    path('posts/create/', views.create_post, name='create_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),

]
from django.urls import path
from . import views

urlpatterns = [
    # 🏠 DASHBOARD (MAIN PAGE)
    path('', views.posts_home, name='posts_home'),   # ✅ FIXED

    # ➕ CREATE POST
    path('create/', views.create_post, name='create_post'),

    # 👤 MY POSTS
    path('my-posts/', views.my_posts, name='my_posts'),

    # ✏️ EDIT POST
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),

    # 🗑 DELETE POST
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
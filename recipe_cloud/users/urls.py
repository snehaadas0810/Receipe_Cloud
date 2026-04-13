from django.urls import path
from . import views

urlpatterns = [
    # 🔥 LANDING PAGE
    path('', views.index, name='index'),   # ✅ FIXED

    # 🔐 AUTH
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🔑 PASSWORD
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # ℹ️ STATIC PAGES
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
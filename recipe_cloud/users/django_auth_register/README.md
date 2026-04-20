# Django Auth Register 🔐

A reusable Django authentication package.

## Features

* User Registration
* Login Validation
* Secure Password Handling
* Security Question Support

## Installation

pip install django-auth-register-sneha

## Usage

Add to INSTALLED_APPS:

INSTALLED_APPS = [
"django_auth_register",
]

Add URLs:

from django.urls import include, path

urlpatterns = [
path("auth/", include("django_auth_register.urls")),
]

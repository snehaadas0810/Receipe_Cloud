from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    security_question = models.CharField(max_length=255, blank=True)
    security_answer = models.CharField(max_length=255, blank=True)

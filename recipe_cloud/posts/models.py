from django.db import models
from django.conf import settings
import os

User = settings.AUTH_USER_MODEL

def validate_media(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4']
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError('Only images and videos allowed')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to='posts/')
    media_type = models.CharField(max_length=10, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        ext = os.path.splitext(self.media.name)[1].lower()

        if ext in ['.jpg', '.jpeg', '.png']:
            self.media_type = 'image'
        else:
            self.media_type = 'video'

        super().save(*args, **kwargs)

class Ingredient(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=255)
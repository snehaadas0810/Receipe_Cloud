from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError


User = settings.AUTH_USER_MODEL


def validate_media(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4']
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError('Only images and videos allowed')
    
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media = models.FileField(upload_to='posts/', validators=[validate_media])
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# def is_video(self): 
#     return self.media.url.endswith('.mp4')

@property
def is_video(self):
    return str(self.media).endswith('.mp4')

def is_image(self):
    return self.media.url.endswith(('.jpg', '.jpeg', '.png'))
    
# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     media = models.FileField(upload_to='posts/')
#     description = models.TextField(blank=True)
#     ingredients = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         ext = os.path.splitext(self.media.name)[1].lower()

#         if ext in ['.jpg', '.jpeg', '.png']:
#             self.media_type = 'image'
#         else:
#             self.media_type = 'video'

#         super().save(*args, **kwargs)

class Ingredient(models.Model):
        post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
        name = models.CharField(max_length=255)

from django.db import models
from django.conf import settings


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Veg'),
        ('nonveg', 'Non-Veg'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media = models.FileField(upload_to='posts/')
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)

    # ✅ FIX: make optional to avoid crash
    processtomake = models.TextField(blank=True, null=True)

    # ✅ FIX: default added to avoid empty error
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='veg')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.description[:20]}"


class Ingredient(models.Model):
    # ✅ FIX: add related_name for easy access
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ingredient_list')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
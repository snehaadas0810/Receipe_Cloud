from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import os


def validate_media(file):
    """
    Validate uploaded file extension (images & videos only)
    """
    valid_extensions = [".jpg", ".jpeg", ".png", ".mp4"]
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError("Only image and video files are allowed.")


class Post(models.Model):
    """
    Model representing a recipe post uploaded by users
    """

    CATEGORY_CHOICES = [
        ("veg", "Veg"),
        ("nonveg", "Non-Veg"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    media = models.FileField(
        upload_to="posts/",
        validators=[validate_media]
    )
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)

    # Optional field for cooking steps
    processtomake = models.TextField(blank=True, null=True)

    # Category with default value
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default="veg"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_video(self):
        """
        Check if uploaded file is a video
        """
        return str(self.media).lower().endswith(".mp4")

    def is_image(self):
        """
        Check if uploaded file is an image
        """
        return str(self.media).lower().endswith((".jpg", ".jpeg", ".png"))

    def __str__(self):
        return f"{self.user} - {self.description[:20]}"


class Ingredient(models.Model):
    """
    Model representing ingredients linked to a post
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="ingredient_list"
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

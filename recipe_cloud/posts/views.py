"""
posts/views.py — Recipe Cloud
Production-ready version with logging, security, and clean structure
"""

import csv
import io
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from aws_libs.s3_service import S3Service
from aws_libs.storage_service import StorageService

from .models import Post


# Initialize logger
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────
# HOME / DASHBOARD
# ─────────────────────────────────────────────────────────────────
def posts_home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "users/home.html", {"posts": posts})


# ─────────────────────────────────────────────────────────────────
# CREATE POST
# ─────────────────────────────────────────────────────────────────
@login_required
def create_post(request):
    if request.method == "POST":
        media = request.FILES.get("media")
        description = request.POST.get("description")
        ingredients = request.POST.get("ingredients")
        category = request.POST.get("category") or "veg"
        processtomake = request.POST.get("processtomake")

        if not media:
            messages.error(request, "Please upload an image or video.")
            return render(request, "posts/create_post.html")

        try:
            Post.objects.create(
                user=request.user,
                media=media,
                description=description,
                ingredients=ingredients,
                processtomake=processtomake,
                category=category,
            )
            messages.success(request, "Post created successfully!")
            return redirect("posts_home")

        except Exception as e:
            logger.error(f"Error creating post for user {request.user.id}: {e}")
            messages.error(request, "Something went wrong. Please try again.")

    return render(request, "posts/create_post.html")


# ─────────────────────────────────────────────────────────────────
# MY POSTS
# ─────────────────────────────────────────────────────────────────
@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user).order_by("-created_at")

    storage = StorageService()

    for post in posts:
        try:
            post.media_exists = storage.file_exists(str(post.media))
        except Exception as e:
            logger.warning(
                f"Media check failed for post {post.id}: {e}"
            )
            post.media_exists = False

    return render(request, "posts/my_posts.html", {"posts": posts})


# ─────────────────────────────────────────────────────────────────
# EDIT POST
# ─────────────────────────────────────────────────────────────────
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.description = request.POST.get("description")
        post.ingredients = request.POST.get("ingredients")
        post.processtomake = request.POST.get("processtomake")
        post.category = request.POST.get("category") or "veg"

        if request.FILES.get("media"):
            storage = StorageService()

            # Delete old file safely
            try:
                storage.delete_media_file(str(post.media))
            except Exception as e:
                logger.warning(
                    f"Failed to delete old media for post {post.id}: {e}"
                )

            post.media = request.FILES.get("media")

        try:
            post.save()
            messages.success(request, "Post updated successfully!")
            return redirect("my_posts")

        except Exception as e:
            logger.error(f"Error updating post {post.id}: {e}")
            messages.error(request, "Failed to update post.")

    return render(request, "posts/edit_post.html", {"post": post})


# ─────────────────────────────────────────────────────────────────
# DELETE POST
# ─────────────────────────────────────────────────────────────────
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    storage = StorageService()

    try:
        storage.delete_media_file(str(post.media))
    except Exception as e:
        logger.warning(
            f"Failed to delete media for post {post.id}: {e}"
        )

    try:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    except Exception as e:
        logger.error(f"Error deleting post {post.id}: {e}")
        messages.error(request, "Failed to delete post.")

    return redirect("my_posts")


# ─────────────────────────────────────────────────────────────────
# EXPORT POSTS → CSV → S3
# ─────────────────────────────────────────────────────────────────
@login_required
def export_posts(request):
    if request.method == "POST":
        try:
            # Build CSV
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["User", "Description", "Category", "Created At"])

            posts = Post.objects.filter(user=request.user)

            for post in posts:
                writer.writerow(
                    [
                        post.user.username,
                        post.description,
                        post.category,
                        post.created_at,
                    ]
                )

            csv_bytes = output.getvalue().encode("utf-8")

            # Upload to S3
            s3 = S3Service()
            result = s3.upload_csv(
                content_bytes=csv_bytes,
                s3_key=f"backups/{request.user.username}_posts.csv",
            )

            if result.get("success"):
                logger.info(f"S3 upload success: {result.get('url')}")
            else:
                logger.error(f"S3 upload failed: {result.get('error')}")

            # Return file download
            response = HttpResponse(csv_bytes, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="my_posts.csv"'
            return response

        except Exception as e:
            logger.error(f"Export failed for user {request.user.id}: {e}")
            messages.error(request, "Failed to export posts.")
            return redirect("my_posts")

    return redirect("my_posts")

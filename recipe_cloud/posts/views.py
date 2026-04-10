from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Ingredient


# ✅ CREATE POST
@login_required
def create_post(request):
    if request.method == "POST":
        media = request.FILES.get('media')
        description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')

        Post.objects.create(
            user=request.user,
            media=media,
            description=description,
            ingredients=ingredients
        )

        return redirect('home')  # VERY IMPORTANT

    return render(request, 'posts/create_post.html')


# ✅ DELETE POST (ONLY OWN POSTS)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()
    return redirect('home')
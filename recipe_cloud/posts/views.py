from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Ingredient


# ✅ CREATE POST
@login_required
def create_post(request):
    if request.method == 'POST':
        media = request.FILES.get('media')
        description = request.POST.get('description')

        # Create Post
        post = Post.objects.create(
            user=request.user,
            media=media,
            description=description
        )

        # Save Ingredients
        ingredients = [
            request.POST.get('ingredient1'),
            request.POST.get('ingredient2'),
            request.POST.get('ingredient3'),
        ]

        for item in ingredients:
            if item:
                Ingredient.objects.create(post=post, name=item)

        return redirect('home')

    return render(request, 'posts/create_post.html')


# ✅ DELETE POST (ONLY OWN POSTS)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()
    return redirect('home')
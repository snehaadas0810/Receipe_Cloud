from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post


@login_required
def create_post(request):
    if request.method == 'POST':
        media = request.FILES.get('media')
        description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')
        category = request.POST.get('category')
        processtomake = request.POST.get('processtomake')

        # ✅ Prevent empty upload crash
        if not media:
            return render(request, 'posts/create_post.html', {
                'error': 'Please upload an image or video'
            })

        # ✅ Create post safely
        Post.objects.create(
            user=request.user,
            media=media,
            description=description,
            ingredients=ingredients,
            category=category if category else 'veg',  # fallback
            processtomake=processtomake
        )

        return redirect('home')

    return render(request, 'posts/create_post.html')
# ✅ DELETE POST (ONLY OWNER CAN DELETE)
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('home')


from django.contrib.auth.decorators import login_required

@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'posts/my_posts.html', {'posts': posts})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.description = request.POST.get('description')
        post.ingredients = request.POST.get('ingredients')
        post.processtomake = request.POST.get('processtomake')
        post.category = request.POST.get('category')

        if request.FILES.get('media'):
            post.media = request.FILES.get('media')

        post.save()
        return redirect('my_posts')

    return render(request, 'posts/edit_post.html', {'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()
    return redirect('my_posts')
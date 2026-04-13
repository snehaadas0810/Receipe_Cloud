from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post


# ================= CREATE POST =================
@login_required
def create_post(request):
    if request.method == 'POST':
        media = request.FILES.get('media')
        description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')
        category = request.POST.get('category')
        processtomake = request.POST.get('processtomake')

        # ❌ Prevent empty media upload
        if not media:
            return render(request, 'posts/create_post.html', {
                'error': 'Please upload an image or video'
            })

        # ✅ Create Post
        Post.objects.create(
            user=request.user,
            media=media,
            description=description,
            ingredients=ingredients,
            processtomake=processtomake,
            category=category if category else 'veg'
        )

        # 🔥 Redirect to dashboard (NOT index)
        return redirect('posts_home')   # ⚠️ IMPORTANT

    return render(request, 'posts/create_post.html')


# ================= MY POSTS =================
@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'posts/my_posts.html', {'posts': posts})


# ================= EDIT POST =================
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == 'POST':
        post.description = request.POST.get('description')
        post.ingredients = request.POST.get('ingredients')
        post.processtomake = request.POST.get('processtomake')
        post.category = request.POST.get('category')

        # ✅ Update media only if new file uploaded
        if request.FILES.get('media'):
            post.media = request.FILES.get('media')

        post.save()

        return redirect('my_posts')

    return render(request, 'posts/edit_post.html', {'post': post})


# ================= DELETE POST =================
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    post.delete()

    return redirect('my_posts')



# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Post

# @login_required
# def posts_home(request):
#     posts = Post.objects.all().order_by('-created_at')
#     return render(request, 'home.html', {'posts': posts})
from django.shortcuts import render
from .models import Post

def posts_home(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'users/home.html', {
        'posts': posts
    })
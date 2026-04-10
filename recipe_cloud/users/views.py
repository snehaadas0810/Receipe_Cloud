from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'users/home.html', {'posts': posts})


# ================= REGISTER =================
def register_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        question = request.POST.get('security_question')
        answer = request.POST.get('security_answer')

        # Password match check
        if password != confirm_password:
            return render(request, 'users/register.html', {
                'error': 'Passwords do not match'
            })

        # Check if user exists
        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {
                'error': 'Username already exists'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {
                'error': 'Email already registered'
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = fullname
        user.security_question = question
        user.security_answer = answer.lower()
        user.save()

        login(request, user)
        return redirect('home')

    return render(request, 'users/register.html')


# ================= LOGIN =================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'users/login.html')


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('login')


# ================= HOME =================
from posts.models import Post

def home_view(request):
    posts = Post.objects.all().order_by('-created_at')

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        posts = posts.filter(description__icontains=query)

    if category:
        posts = posts.filter(category=category)

    return render(request, 'users/home.html', {
        'posts': posts
    })

# ================= FORGOT PASSWORD =================
def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        question = request.POST.get('security_question')
        answer = request.POST.get('security_answer')

        try:
            user = User.objects.get(username=username, email=email)

            if (
                user.security_question == question and
                user.security_answer == answer.lower()
            ):
                request.session['reset_user'] = user.id
                return redirect('reset_password')
            else:
                return render(request, 'users/forgot_password.html', {
                    'error': 'Invalid details'
                })

        except User.DoesNotExist:
            return render(request, 'users/forgot_password.html', {
                'error': 'Invalid details'
            })

    return render(request, 'users/forgot_password.html')


# ================= RESET PASSWORD =================
def reset_password(request):
    user_id = request.session.get('reset_user')

    if not user_id:
        return redirect('forgot_password')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            return render(request, 'users/reset_password.html', {
                'error': 'Passwords do not match'
            })

        user.set_password(password)
        user.save()

        # Clear session after reset
        del request.session['reset_user']

        return redirect('login')

    return render(request, 'users/reset_password.html')
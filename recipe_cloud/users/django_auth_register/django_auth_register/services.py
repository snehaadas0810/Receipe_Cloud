from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()


# ================= CREATE USER =================
def create_user_account(
    fullname,
    username,
    email,
    password,
    confirm_password,
    security_question=None,
    security_answer=None,
):
    """
    Handles user registration logic
    """

    # 🔹 Password match check
    if password != confirm_password:
        raise ValidationError("Passwords do not match")

    # 🔹 Username check
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists")

    # 🔹 Email check
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already registered")

    # 🔹 Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    user.first_name = fullname

    # 🔐 Secure answer (hashed)
    if security_answer:
        user.security_question = security_question
        user.security_answer = make_password(security_answer.lower())

    user.save()

    return user


# ================= AUTH VALIDATION =================
def validate_user_credentials(username, password):
    """
    Validate login credentials
    """
    from django.contrib.auth import authenticate

    user = authenticate(username=username, password=password)

    if user is None:
        raise ValidationError("Invalid username or password")

    return user


# ================= PASSWORD RESET VALIDATION =================
def validate_security_answer(user, question, answer):
    """
    Validate security question & answer
    """
    from django.contrib.auth.hashers import check_password

    if user.security_question != question:
        return False

    return check_password(answer.lower(), user.security_answer)
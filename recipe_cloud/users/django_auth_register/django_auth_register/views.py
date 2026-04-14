from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.exceptions import ValidationError

from .services import create_user_account


def register_view(request):
    if request.method == "POST":
        try:
            user = create_user_account(
                fullname=request.POST.get("fullname"),
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=request.POST.get("password"),
                confirm_password=request.POST.get("confirm_password"),
                security_question=request.POST.get("security_question"),
                security_answer=request.POST.get("security_answer"),
            )

            login(request, user)
            return redirect("/")

        except ValidationError as e:
            return render(request, "register.html", {"error": str(e)})

    return render(request, "register.html")
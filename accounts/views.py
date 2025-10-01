from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def index(request):
    return render(request, "accounts/index.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        phone_number = request.POST["phone_number"]
        national_id = request.POST["national_id"]
        email = request.POST.get("email")  # optional

        # create using our custom manager
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            phone_number=phone_number,
            national_id=national_id,
            email=email,
        )
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")
    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "accounts/login.html")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})

def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("login")

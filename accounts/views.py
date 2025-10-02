from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "accounts/login.html")


@login_required
def profile_view(request):
    context = {
        "user": request.user,
        "pending_loans_count": request.user.loans.filter(status='pending').count(),
        "approved_loans_count": request.user.loans.filter(status='approved').count(),
        "total_borrowed": sum(loan.amount for loan in request.user.loans.all()),
    }
    return render(request, "accounts/profile.html", context)

@login_required
def dashboard_view(request):
    user = request.user
    loans = user.loans.all()
    recent_loans = loans.order_by('-created_at')[:5]
    pending_loans = loans.filter(status='pending')
    
    # Calculate total amounts
    total_amount = loans.aggregate(Sum('amount'))['amount__sum'] or 0
    total_repaid = sum(
        repayment.amount_paid 
        for loan in loans 
        for repayment in loan.repayments_set.all()
    )
    
    context = {
        'total_loans': loans.count(),
        'total_amount': total_amount,
        'total_repaid': total_repaid,
        'recent_loans': recent_loans,
        'pending_loans': pending_loans,
    }
    return render(request, "dashboard.html", context)

def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("login")

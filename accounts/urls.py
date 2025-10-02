from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("logout/", views.logout_view, name="logout"),
]

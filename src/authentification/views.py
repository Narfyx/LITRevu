"""
Views for user authentication and registration.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def inscription(request):
    """
    Handle user registration.

    If the request method is POST, validate and save the registration form.
    Redirect to the user follow page upon successful registration.
    If the request method is GET, display an empty registration form.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_follow")
    else:
        form = CustomUserCreationForm()
    return render(request, "inscription.html", {"form": form})


def connexion(request):
    """
    Handle user login.

    If the request method is POST, authenticate the user with the provided
    username and password. If authentication is successful, log the user in and
    redirect to the appropriate page. If authentication fails, display an error
    message. If the request method is GET, display the login form.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.username == "admin":
                print("OKKKK")
                return redirect("admin/login/?next=/admin/")
            return redirect("flux")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "connexion.html")


@login_required
def deconnexion(request):
    """
    Handle user logout.

    Log the user out and redirect to the login page.
    """
    logout(request)
    return redirect("connexion")

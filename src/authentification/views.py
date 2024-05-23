from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .form import CustomUserCreationForm
from authentification.models import User

def inscription(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_follow")
    else:
        form = CustomUserCreationForm()
    return render(request, "inscription.html", {"form": form})


def connexion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.username == "admin":
                print("OKKKK")
                return redirect("admin/login/?next=/admin/")
            return redirect("user_follow")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "connexion.html")


@login_required
def deconnexion(request):
    logout(request)
    return redirect("connexion")

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def user_follow(request):
    return render(request, 'user_follow.html')


"""

def deconnexion(request):
    logout(request)
    return redirect('connexion') 
"""
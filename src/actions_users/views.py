from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import SearchUserForm

from pprint import pprint
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@login_required
def user_follow(request):
    return render(request, 'user_follow.html')



def search_user(request):
    users_list = []
    
    search_query = request.GET.get('user')

    if search_query:
        users_objs = User.objects.filter(username__icontains=search_query, is_active=True)
        
        for user_obj in users_objs:
            users_list.append(user_obj.username)

    return JsonResponse({'status':200, 'data':users_list})
    #return render(request, 'search.html')  # Assurez-vous que ce template existe
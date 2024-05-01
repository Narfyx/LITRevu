from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from authentification.models import Utilisateur
from .models import UserFollows
from .forms import SearchUserForm


from colorama import Fore
from pprint import pprint

@login_required
def user_follow(request):
    current_user = request.user
    
    followers = UserFollows.objects.filter(followed_user=current_user)
    followers_users = [follower.user for follower in followers]

    followings = UserFollows.objects.filter(user=current_user)
    followed_users = [follow.followed_user for follow in followings]

    return render(request, 'user_follow.html', {'followers': followers_users, 'followed_users': followed_users})


@login_required
def search_user(request):
    current_user = request.user
    users_list = []
    search_query = request.GET.get('user')

    if search_query:
        users_objs = User.objects.filter(username__icontains=search_query, is_active=True)
        for user_obj in users_objs:
            if user_obj.username == 'admin' or user_obj.username == current_user.username:
                continue
            users_list.append(user_obj.username)

    return JsonResponse({'status':200, 'data':users_list})


@login_required
def follow_user(request, username):
    user = request.user
    user_to_follow = get_object_or_404(User, username=username)

    if user.username == user_to_follow.username:
        messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
        return redirect('user_follow')

    _, created = UserFollows.objects.get_or_create(user=user, followed_user=user_to_follow) 
    # _ = instance de UserFollows
    
    if created:
        messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
    else:
        messages.info(request, f"Vous suivez déjà {user_to_follow.username}.")

    return redirect('user_follow')
    

@login_required
def unfollow_user(request, username):
    if request.method == 'POST':
        user = request.user
        user_to_unfollow = get_object_or_404(User, username=username)

        # Vérifier si l'utilisateur tente de se "désabonner" de lui-même (ce qui ne devrait pas arriver)
        if user.username == user_to_unfollow.username:
            messages.error(request, "Vous ne pouvez pas vous désabonner de vous-même.")
            return redirect('user_follow')

        # Trouver la relation de suivi pour la supprimer
        follow_relationship = UserFollows.objects.filter(user=user, followed_user=user_to_unfollow)
        if follow_relationship.exists():
            follow_relationship.delete()
            messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")
        else:
            messages.info(request, f"Vous ne suivez pas {user_to_unfollow.username}.")

    return redirect('user_follow')


    

from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.db.models import Count, OuterRef, Subquery, Q

from .forms import ReviewForm, TicketForm
from .models import Review, Ticket, UserFollows


@login_required
def user_follow(request):
    current_user = request.user

    followers = UserFollows.objects.filter(followed_user=current_user)
    followers_users = [follower.user for follower in followers]

    followings = UserFollows.objects.filter(user=current_user)
    followed_users = [follow.followed_user for follow in followings]

    return render(
        request,
        "user_follow.html",
        {"followers": followers_users, "followed_users": followed_users},
    )


@login_required
def search_user(request):
    current_user = request.user
    users_list = []
    search_query = request.GET.get("user")

    if search_query:
        users_objs = User.objects.filter(
            username__icontains=search_query, is_active=True
        )
        for user_obj in users_objs:
            if (
                user_obj.username == "admin"
                or user_obj.username == current_user.username
            ):
                continue
            users_list.append(user_obj.username)

    return JsonResponse({"status": 200, "data": users_list})

@login_required
def follow_user(request, username):
    user = request.user

    try:
        user_to_follow = User.objects.get(username=username)
        
        if user.username == user_to_follow.username:
            messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
            return redirect("user_follow")
        
        _, created = UserFollows.objects.get_or_create(
            user=user, followed_user=user_to_follow
        )

        if created:
            messages.success(request, f"Vous suivez maintenant {user_to_follow.username}.")
        else:
            messages.info(request, f"Vous suivez déjà {user_to_follow.username}.")
    except User.DoesNotExist:
        messages.error(request, "Cet utilisateur n'existe pas")
    
    return redirect("user_follow")


@login_required
def unfollow_user(request, username):
    if request.method == "POST":
        user = request.user
        user_to_unfollow = get_object_or_404(User, username=username)

        # Vérifier si l'utilisateur tente de se "désabonner" de lui-même (ce qui ne devrait pas arriver)
        if user.username == user_to_unfollow.username:
            messages.error(request, "Vous ne pouvez pas vous désabonner de vous-même.")
            return redirect("user_follow")

        # Trouver la relation de suivi pour la supprimer
        follow_relationship = UserFollows.objects.filter(
            user=user, followed_user=user_to_unfollow
        )
        if follow_relationship.exists():
            follow_relationship.delete()
            messages.success(
                request, f"Vous ne suivez plus {user_to_unfollow.username}."
            )
        else:
            messages.info(request, f"Vous ne suivez pas {user_to_unfollow.username}.")

    return redirect("user_follow")


@login_required
def flux(request):
    user = request.user
    
    following = UserFollows.objects.filter(user=user)
    followed_users = [follow.followed_user for follow in following]
    followed_users.append(user)
    
    user_review_count = Review.objects.filter(ticket=OuterRef('pk'), user=user).values('ticket').annotate(count=Count('id')).values('count')
    
    tickets = Ticket.objects.filter(user__in=followed_users).annotate(user_review_count=Subquery(user_review_count))
    reviews = Review.objects.filter(user__in=followed_users)
    
    # Combine et trie les tickets et les reviews par date de création
    posts = sorted(
        list(tickets) + list(reviews), key=lambda post: post.time_created, reverse=True
    )
    
    context = {
        'posts': posts
    }
    return render(request, "flux.html", context)


@login_required
def my_post(request):
    user = request.user

    user_review_count = Review.objects.filter(ticket=OuterRef('pk'), user=user).values('ticket').annotate(count=Count('id')).values('count')

    tickets = Ticket.objects.filter(user=user).annotate(user_review_count=Subquery(user_review_count))
    reviews = Review.objects.filter(user=user)
    

    posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created, reverse=True
    )

    content = {"posts": posts}
    print(content)
    return render(request, "my_post.html", context=content)


@login_required
def create_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("my_post")
    else:
        ticket_form = TicketForm()
    return render(request, "user_create_ticket.html", {"ticket_form": ticket_form})


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket  # Associer le ticket à la revue
            review.save()
            return redirect("my_post")
    else:
        review_form = ReviewForm()
    
    return render(request, "user_create_review.html", {"review_form": review_form, "ticket": ticket})

@login_required
def create_ticket_and_review(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            review = review_form.save(commit=False)
            ticket.user = request.user
            review.user = request.user

            ticket.save()
            review.ticket = ticket  # Assigner le ticket à la revue
            review.save()
            return redirect("my_post")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {"review_form": review_form, "ticket_form": ticket_form}
    return render(request, "user_create_ticket_and_review.html", context=context)


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        edit_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect("my_post")
    else:
        edit_form = TicketForm(instance=ticket)

    return render(request, "user_edit_ticket.html", {"edit_form": edit_form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("my_post")
    else:
        review_form = ReviewForm(instance=review)

    return render(request, "user_edit_review.html", {"review_form": review_form})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user == ticket.user:
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès.")
    else:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce ticket.")
    return redirect("my_post")

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
        messages.success(request, "La critique a été supprimée avec succès.")
    else:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette critique.")
    return redirect("my_post")
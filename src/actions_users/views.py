"""
Views for user interactions including follow, search, create, edit, and delete tickets and reviews.
"""

from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, OuterRef, Subquery
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm, TicketForm
from .models import Review, Ticket, UserFollows


@login_required
def user_follow(request):
    """
    View to manage user follow and unfollow actions.

    Retrieves the list of followers and followed users for the current user.
    """
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
    """
    View to search for users by username.

    Returns a JSON response with a list of matching usernames.
    """
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
    """
    View to follow another user.

    If the user exists and is not the current user, create a follow relationship.
    """
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
            messages.success(
                request, f"Vous suivez maintenant {user_to_follow.username}."
            )

        else:
            messages.info(request, f"Vous suivez déjà {user_to_follow.username}.")
    except User.DoesNotExist:
        messages.error(request, "Cet utilisateur n'existe pas")

    return redirect("user_follow")


@login_required
def unfollow_user(request, username):
    """
    View to unfollow a user.

    If the user exists and is currently followed by the current user, delete the follow relationship.
    """
    if request.method == "POST":
        user = request.user
        user_to_unfollow = get_object_or_404(User, username=username)

        if user.username == user_to_unfollow.username:
            messages.error(request, "Vous ne pouvez pas vous désabonner de vous-même.")
            return redirect("user_follow")

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
    """
    View to display the feed of tickets and reviews from followed users and the current user.
    """
    user = request.user

    following = UserFollows.objects.filter(user=user)
    followed_users = [follow.followed_user for follow in following]
    followed_users.append(user)

    user_review_count = (
        Review.objects.filter(ticket=OuterRef("pk"), user=user)
        .values("ticket")
        .annotate(count=Count("id"))
        .values("count")
    )

    tickets = Ticket.objects.filter(user__in=followed_users).annotate(
        user_review_count=Subquery(user_review_count)
    )
    reviews = Review.objects.filter(user__in=followed_users)

    posts = sorted(
        list(tickets) + list(reviews), key=lambda post: post.time_created, reverse=True
    )

    context = {"posts": posts}
    return render(request, "flux.html", context)


@login_required
def my_post(request):
    """
    View to display the current user's tickets and reviews.
    """
    user = request.user

    user_review_count = (
        Review.objects.filter(ticket=OuterRef("pk"), user=user)
        .values("ticket")
        .annotate(count=Count("id"))
        .values("count")
    )

    tickets = Ticket.objects.filter(user=user).annotate(
        user_review_count=Subquery(user_review_count)
    )
    reviews = Review.objects.filter(user=user)

    posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created, reverse=True
    )

    content = {"posts": posts}
    return render(request, "my_post.html", context=content)


@login_required
def create_ticket(request):
    """
    View to create a new ticket.

    Displays a form for creating a ticket and handles form submission.
    """
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
    """
    View to create a new review for a specific ticket.

    Displays a form for creating a review and handles form submission.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("my_post")
    else:
        review_form = ReviewForm()

    return render(
        request,
        "user_create_review.html",
        {"review_form": review_form, "ticket": ticket},
    )


@login_required
def create_ticket_and_review(request):
    """
    View to create a new ticket and review in a single form submission.

    Displays forms for creating a ticket and a review and handles their submission.
    """
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            review = review_form.save(commit=False)
            ticket.user = request.user
            review.user = request.user

            ticket.save()
            review.ticket = ticket
            review.save()
            return redirect("my_post")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {"review_form": review_form, "ticket_form": ticket_form}
    return render(request, "user_create_ticket_and_review.html", context=context)


@login_required
def ticket_edit(request, ticket_id):
    """
    View to edit an existing ticket.

    Displays a form for editing a ticket and handles form submission.
    """
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
    """
    View to edit an existing review.

    Displays a form for editing a review and handles form submission.
    """
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
    """
    View to delete an existing ticket.

    Deletes the ticket if the current user is the owner and redirects to the user's posts.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user == ticket.user:
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès.")
    else:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce ticket.")
    return redirect("my_post")


@login_required
def delete_review(request, review_id):
    """
    View to delete an existing review.

    Deletes the review if the current user is the owner and redirects to the user's posts.
    """
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
        messages.success(request, "La critique a été supprimée avec succès.")
    else:
        messages.error(
            request, "Vous n'avez pas la permission de supprimer cette critique."
        )
    return redirect("my_post")

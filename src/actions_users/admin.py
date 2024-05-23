"""
Admin configuration for the authentification app.
"""

from django.contrib import admin

from .models import Review, Ticket, UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    """
    Admin view for the UserFollows model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
    """

    list_display = ("user", "followed_user")


class TicketAdmin(admin.ModelAdmin):
    """
    Admin view for the Ticket model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
    """

    list_display = ("title", "user", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    """
    Admin view for the Review model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
    """

    list_display = ("ticket", "rating", "user", "time_created")


# Register the models with the custom admin views
admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)

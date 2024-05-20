from django.contrib import admin

from .models import Review, Ticket, UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("ticket", "rating", "user", "time_created")


admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)

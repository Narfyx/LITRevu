from django import forms

from .models import Review, Ticket


class SearchUserForm(forms.Form):
    search_query = forms.CharField(label="Rechercher", max_length=100)


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "rating": forms.RadioSelect(
                choices=[
                    (0, " -0"),
                    (1, " -1"),
                    (2, " -2"),
                    (3, " -3"),
                    (4, " -4"),
                    (5, " -5"),
                ],
            )
        }

from django import forms

from . import models


class SearchUserForm(forms.Form):
    search_query = forms.CharField(label="Rechercher", max_length=100)


class TicketForm(forms.ModelForm):

    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]
        labels = {"title": "Titre"}


class DeleteTicketForm(forms.Form):

    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

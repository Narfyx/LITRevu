from django import forms


class SearchUserForm(forms.Form):
    search_query = forms.CharField(label="Rechercher", max_length=100)

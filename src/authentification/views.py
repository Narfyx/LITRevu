from django.shortcuts import render

def index(request):
    return render(request, "authentification/connection_page.html")


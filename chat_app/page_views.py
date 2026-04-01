from django.shortcuts import render
from django.http import HttpResponse
"""
def index_view(request):
    return HttpResponse("index ok")
"""
def index_view(request):
    return render(request, "index.html")

def register_page_view(request):
    return render(request, "register.html")

def home_view(request):
    return render(request, "home.html")

def conversation_page_view(request, conversation_id):
    username = request.GET.get("username")
    return render(request, "conversation.html", {
        "username": username,
        "conversation_id": conversation_id
    })
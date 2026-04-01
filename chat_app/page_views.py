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
    return render(request, "conversation.html", {
        "conversation_id": conversation_id
    })
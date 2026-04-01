from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from chat_app.repositories.message_repository import get_messages_by_conversation

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
    messages = get_messages_by_conversation(conversation_id)
    
    # Debug : Regarde dans ton terminal si "messages" contient quelque chose
    print(f"Nombre de messages trouvés : {len(messages)}")

    history_text = ""
    for msg in messages:
        # On essaie de récupérer le nom de l'envoyeur
        # Si tu n'as pas le nom, utilise une valeur par défaut pour tester
        sender = msg.get('sender_username', 'Inconnu') 
        content = msg.get('content', '')
        if content:
            history_text += f"{sender}: {content}\n"

    return render(request, "conversation.html", {
        "conversation_id": conversation_id,
        "history": history_text # On envoie le texte au HTML
    })
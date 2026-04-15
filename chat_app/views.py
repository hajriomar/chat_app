from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.http import JsonResponse
from .db.mongo import users_collection
from .db.redis_client import redis_client
from chat_app.services.chat_service import get_user_conversations, create_group_conversation
from chat_app.repositories.message_repository import get_most_active_users,get_most_solicited_users,get_groups_and_members
import traceback
from chat_app.services.user_service import (
    register_user,
    authenticate_user,
    get_online_friends_for_user,
    get_available_users_for_invitation,
    send_friend_request,
    get_received_friend_requests,
    accept_friend_request,
)
<<<<<<< HEAD
from chat_app.services.chat_service import get_user_conversations,get_conversation_messages
=======
from chat_app.repositories.redis_repository import (
    get_online_users, 
    get_total_logins, 
    get_global_activity_history, 
    get_all_users_total_time
)
from chat_app.services.chat_service import get_user_conversations
>>>>>>> mariem
from chat_app.services.presence_service import login_user, logout_user, list_online_users

@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "email": {"type": "string"},
                "password": {"type": "string"},
                "full_name": {"type": "string"},
            },
            "required": ["username", "email", "password", "full_name"],
        }
    },
    responses={201: dict},
    examples=[
        OpenApiExample(
            "Exemple inscription",
            value={
                "username": "souha",
                "email": "souha@gmail.com",
                "password": "123456",
                "full_name": "Souha Gharsallah"
            },
        )
    ],
)
@api_view(["POST"])
def register_view(request):
    data = request.data
    try:
        user_id = register_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            full_name=data["full_name"]
        )
        return Response({"message": "Utilisateur créé", "user_id": user_id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
            },
            "required": ["username"],
        }
    },
    responses={200: dict},
)
@api_view(["POST"])
def login_view(request):
    data = request.data
    login_user(data["username"])
    return Response({"message": "Utilisateur connecté"})


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {"username": {"type": "string"}},
            "required": ["username"],
        }
    },
    responses={200: dict},
)
@api_view(["POST"])
def logout_view(request):
    try:
        data = request.data
        username = data.get("username")
        
        # Sécurité : on vérifie que le nom est bien reçu
        if not username:
            return Response({"error": "Nom d'utilisateur manquant dans la requête"}, status=status.HTTP_400_BAD_REQUEST)

        # La fonction qui crashe potentiellement
        logout_user(username)
        
        return Response({"message": f"Utilisateur {username} déconnecté"}, status=status.HTTP_200_OK)
        
    except Exception as e:
        # On capture le crash exact et on l'imprime !
        traceback.print_exc() 
        return Response({
            "error": "Alerte Crash Django", 
            "detail": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(responses={200: dict})
@api_view(["GET"])
def online_users_view(request):
    users = list_online_users()
    return Response({"online_users": users})


@api_view(["POST"])
def login_page_view(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    # 1. Vérification spécifique pour le compte administrateur
    if username == "admin" and password == "admin":
        login_user("admin") # On marque l'admin comme "online" dans Redis
        return Response({
            "message": "Connexion administrateur réussie",
            "username": "admin",
            "is_admin": True  # Signal pour le frontend
        }, status=status.HTTP_200_OK)

    # 2. Logique normale pour les autres utilisateurs
    try:
        user = authenticate_user(
            username=username,
            password=password
        )

        login_user(user["username"])

        return Response({
            "message": "Connexion réussie",
            "username": user["username"],
            "is_admin": False
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def online_friends_view(request):
    username = request.GET.get("username")
    data = get_online_friends_for_user(username)
    return Response({"online_friends": data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def conversations_list_view(request):
    username = request.GET.get("username")
    data = get_user_conversations(username)
    return Response({"conversations": data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def available_users_view(request):
    username = request.GET.get("username")
    data = get_available_users_for_invitation(username)
    return Response({"users": data}, status=status.HTTP_200_OK)


@api_view(["POST"])
def send_friend_request_view(request):
    data = request.data

    try:
        send_friend_request(
            sender_username=data["sender_username"],
            receiver_username=data["receiver_username"]
        )
        return Response({"message": "Invitation envoyée"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def received_requests_view(request):
    username = request.GET.get("username")

    try:
        data = get_received_friend_requests(username)
        return Response({"requests": data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def accept_friend_request_view(request):
    data = request.data

    try:
        accept_friend_request(
            current_username=data["current_username"],
            sender_username=data["sender_username"]
        )
        return Response({"message": "Invitation acceptée"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
<<<<<<< HEAD
def get_conversation_messages_view(request, conversation_id):
    username = request.GET.get("username")

    if not username:
        return Response(
            {"error": "username requis"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        messages = get_conversation_messages(username, conversation_id)
        return Response(
            {"messages": messages},
            status=status.HTTP_200_OK
        )
    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
=======
def get_friends(request):
    username = request.GET.get("username")

    if not username:
        return Response({"error": "username manquant"}, status=status.HTTP_400_BAD_REQUEST)

    current_user = users_collection.find_one({"username": username})

    if not current_user:
        return Response({"error": "utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

    online_users = set(list_online_users())
    friends_ids = current_user.get("friends", [])
    friends_data = []

    for friend_id in friends_ids:
        friend = users_collection.find_one({"_id": friend_id})

        if friend:
            friend_username = friend.get("username")

            friends_data.append({
                "username": friend_username,
                "online": friend_username in online_users
            })

    return Response({"friends": friends_data}, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_group_view(request):
    data = request.data

    try:
        conversation_id = create_group_conversation(
            creator_username=data["creator"],
            participants_usernames=data["participants"],
            group_name=data["group_name"]
        )

        return Response({
            "success": True,
            "conversation_id": str(conversation_id)
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
#AJOUT
@api_view(["GET"])
def admin_stats_api(request):
    try:
        # Récupération des données brutes
        online_users = get_online_users()
        # Décodage des utilisateurs en ligne (au cas où Redis renvoie des bytes)
        online_users_decoded = [u.decode('utf-8') if isinstance(u, bytes) else u for u in online_users]
        
        total_logins = get_total_logins()
        if isinstance(total_logins, bytes):
            total_logins = total_logins.decode('utf-8')
            
        raw_activities = get_global_activity_history()
        
        # Formatage de l'historique (username|action|timestamp)
        formatted_activities = []
        for act in raw_activities:
            parts = act.split('|')
            # On vérifie si on a 3 (login) ou 4 (logout avec durée) parties
            if len(parts) >= 3:
                formatted_activities.append({
                    "username": parts[0],
                    "action": parts[1],
                    "timestamp": parts[2],
                    "duration": parts[3] if len(parts) > 3 else None # Récupère la durée
                })
        most_active = get_most_active_users(3)
        most_popular = get_most_solicited_users(3) # Utilise la fonction de sollicitation
        groups_list = get_groups_and_members()
        users_time = get_all_users_total_time()
        return Response({
            "online_count": len(online_users_decoded),
            "online_users": online_users_decoded,
            "total_logins": int(total_logins) if total_logins else 0,
            "recent_activity": formatted_activities,
            "most_active_users": most_active,
            "most_popular": most_popular, 
            "groups_list": groups_list,
            "users_time": users_time
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        traceback.print_exc()  # ← Affiche l'erreur complète dans la console Django
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
>>>>>>> mariem

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample

from chat_app.services.user_service import (
    register_user,
    authenticate_user,
    get_online_friends_for_user,
    get_available_users_for_invitation,
    send_friend_request,
    get_received_friend_requests,
    accept_friend_request,
)
from chat_app.services.chat_service import get_user_conversations
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
            "properties": {
                "username": {"type": "string"},
            },
            "required": ["username"],
        }
    },
    responses={200: dict},
)
@api_view(["POST"])
def logout_view(request):
    data = request.data
    logout_user(data["username"])
    return Response({"message": "Utilisateur déconnecté"})


@extend_schema(responses={200: dict})
@api_view(["GET"])
def online_users_view(request):
    users = list_online_users()
    return Response({"online_users": users})


@api_view(["POST"])
def login_page_view(request):
    data = request.data

    try:
        user = authenticate_user(
            username=data["username"],
            password=data["password"]
        )

        login_user(user["username"])

        return Response({
            "message": "Connexion réussie",
            "username": user["username"]
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
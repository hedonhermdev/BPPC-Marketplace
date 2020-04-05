from django.contrib.auth.models import User
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as googleIdToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.auth_helpers import generate_random_password, get_jwt_with_user


@api_view(["POST"])
def login(request):
    try:
        id_token = request.data["id_token"]
    except KeyError:
        return Response(
            {"error": "No id_token provided"}, status=status.HTTP_403_FORBIDDEN
        )

    id_info = googleIdToken.verify_oauth2_token(id_token, google_requests.Request())

    if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response(
            {"error": "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN
        )

    email = id_info["email"]

    domain = getattr(id_info, "hd", email.split("@")[-1])

    if domain != "pilani.bits-pilani.ac.in":
        return Response(
            {"error": "Not a valid BITS Mail account"}, status=status.HTTP_403_FORBIDDEN
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Account not found. You must register first."},
            status=status.HTTP_403_FORBIDDEN,
        )

    token = get_jwt_with_user(user)

    return Response({"token": token}, status=status.HTTP_200_OK)


@api_view(["POST"])
def register(request):
    try:
        id_token = request.data["id_token"]
    except KeyError:
        return Response(
            {"error": "No id_token provided"}, status=status.HTTP_403_FORBIDDEN
        )

    id_info = googleIdToken.verify_oauth2_token(id_token, google_requests.Request())

    if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response(
            {"error": "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN
        )

    email = id_info["email"]

    domain = getattr(id_info, "hd", email.split("@")[-1])

    if domain != "pilani.bits-pilani.ac.in":
        return Response(
            {"error": "Not a valid BITS Mail account"}, status=status.HTTP_403_FORBIDDEN
        )

    user = User(username=email.split("@")[0], email=email)
    user.set_password(generate_random_password())

    user.save()

    token = get_jwt_with_user(user)

    return Response(
        {"token": token, "username": user.username, "email": user.email},
        status=status.HTTP_201_CREATED,
    )

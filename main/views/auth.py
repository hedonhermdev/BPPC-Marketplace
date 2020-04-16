from django.contrib.auth.models import User
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as googleIdToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.auth_helpers import generate_random_password, get_jwt_with_user

import logging

log = logging.getLogger("main")


@api_view(['POST'])
def authenticate(request):
    try:
        id_token = request.data["id_token"]
    except KeyError:
        log.error(f"{request.path}: no id_token provided in request body. ")
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
        log.error(f"{request.path}: {email} is not a valid BITS Mail account")
        return Response(
            {"error": "Not a valid BITS Mail account"}, status=status.HTTP_403_FORBIDDEN
        )

    if User.objects.filter(email=email).count() != 0:
        user = User.objects.get(email=email)
        token = get_jwt_with_user(user)
        log.info(f"{request.path}: user {user.username} logged in.")
        return Response({"token": token, "isNew": False}, status=status.HTTP_200_OK)

    user = User(username=email.split("@")[0], email=email)
    user.set_password(generate_random_password())

    user.save()

    token = get_jwt_with_user(user)

    log.info(f"{request.path}: created user with email {user.email}")
    return Response(
        {"token": token, "username": user.username, "email": user.email, "isNew": True},
        status=status.HTTP_201_CREATED,
    )


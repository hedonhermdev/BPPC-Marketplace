from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as googleIdToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.auth_helpers import generate_random_password, get_jwt_with_user
from main.models import User, Profile

import logging

# Set up logger. 
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

    # Login if user already exists.
    if User.objects.filter(email=email).count() != 0:
        user = User.objects.get(email=email)
        token = get_jwt_with_user(user)
        log.info(f"{request.path}: user {user.username} logged in.")
        return Response({"token": token, "isNew": False}, status=status.HTTP_200_OK)

    domain = getattr(id_info, "hd", email.split("@")[-1])

    # Bitsian or Non Bitsian
    if domain == "pilani.bits-pilani.ac.in":
        # Bitsians can be sellers
        permission_level = Profile.SELLER
    else:
        # Non-bitsians can be buyers only.
        permission_level = Profile.BUYER


    user = User(username=email.split("@")[0], email=email)
    user.set_password(generate_random_password())
    user.save()
    user.profile.permission_level = permission_level   
    user.profile.save()
    token = get_jwt_with_user(user)

    log.info(f"{request.path}: created user with email {user.email}")
    return Response(
        {"token": token, "username": user.username, "email": user.email, "isNew": True},
        status=status.HTTP_201_CREATED,
    )


import random
from django.contrib.auth.decorators import user_passes_test
from rest_framework_jwt.settings import api_settings
from main.models import User


def generate_random_password():

    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p = "".join(random.sample(s, passlen))

    return p


def get_jwt_with_user(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

def create_user_from_email(email):
    username, _ = email.split("@")
    user = User(username=username, email=email)
    user.save()
    password = generate_random_password()
    user.profile.email = email
    user.profile.save()
    return user

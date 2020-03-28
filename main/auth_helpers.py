import random

from rest_framework_jwt.settings import api_settings

def generate_random_password():

    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p = "".join(random.sample(s,passlen))

    return p

def get_jwt_with_user(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER 
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token




    


from rest_framework.response import Response

def index(request):
    return Response("If you can see this, then the backend server is (hopefully) working. \n\t\t\t\t- Tirth Jain")

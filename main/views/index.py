from django.http import HttpResponse
def index(request):
    return HttpResponse("If you can see this, then the backend server is (hopefully) working. \n\t\t\t\t- Tirth Jain")

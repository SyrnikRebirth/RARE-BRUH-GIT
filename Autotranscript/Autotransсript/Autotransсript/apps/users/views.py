from django.http import HttpResponse

def index(request):
    return HttpResponse("Это страница польователя!")

# Create your views here.

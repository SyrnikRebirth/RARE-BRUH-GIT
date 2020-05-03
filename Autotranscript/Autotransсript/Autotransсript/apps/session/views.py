from django.http import HttpResponse

def index(request):
    return HttpResponse("Это страница сессии!")

# Create your views here.

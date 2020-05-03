from django.http import HttpResponse

def index(request):
    return HttpResponse("Это страница регистрации!")

# Create your views here.

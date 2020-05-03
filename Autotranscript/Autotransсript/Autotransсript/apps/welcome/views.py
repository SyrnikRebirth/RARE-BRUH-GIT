from django.http import HttpResponse

def index(request):
    return HttpResponse("Это стартовая страница!")

# Create your views here.

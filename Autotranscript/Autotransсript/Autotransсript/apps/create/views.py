from django.shortcuts import render

def index(request):
    return render(request, 'create/create_page.html')

# Create your views here.

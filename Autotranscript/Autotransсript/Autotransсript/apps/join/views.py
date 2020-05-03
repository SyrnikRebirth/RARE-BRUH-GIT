from django.shortcuts import render

def index(request):
    return render(request, 'join/join_page.html')

# Create your views here.

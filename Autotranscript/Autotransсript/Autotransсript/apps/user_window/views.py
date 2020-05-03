from django.shortcuts import render

def index(request):
    return render(request, 'user_window/u_window.html')

# Create your views here.

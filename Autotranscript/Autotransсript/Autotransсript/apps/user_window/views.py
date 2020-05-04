from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='http://127.0.0.1:8000/login/')
def index(request):
    return render(request, 'user_window/u_window.html')

# Create your views here.

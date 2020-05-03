from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'auth/auth_form.html')
# Create your views here.

from django.shortcuts import render

def index(request):
    return render(request, 'welcome/Welcome_page.html')

# Create your views here.

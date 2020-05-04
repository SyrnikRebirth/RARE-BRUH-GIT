from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import speach_to_text

@login_required(login_url='http://127.0.0.1:8000/login/')
def index(request):
    return render(request, 'chat/chat_page.html')

@login_required(login_url='http://127.0.0.1:8000/login/')
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
# Create your views here.

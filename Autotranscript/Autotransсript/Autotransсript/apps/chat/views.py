from django.shortcuts import render

def index(request):
    return render(request, 'chat/chat_page.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

# Create your views here.

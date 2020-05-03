from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/user_window/')
        else:
            messages.info(request, 'Неверное имя пользователя или пароль')
            return render(request, 'login/log_page.html')
    context = {}
    return render(request, 'login/log_page.html', context)

def logoutUser(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/login/')

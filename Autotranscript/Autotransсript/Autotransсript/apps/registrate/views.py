from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages

def index(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Аккаунт '+ user +' успешно создан!')
            return redirect('http://127.0.0.1:8000/login/')
    context = {'form': form}
    return render(request, 'registrate/registrate_page.html', context)

# Create your views here.

from django.shortcuts import render, redirect
from . forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User,auth


def home(request):
    return render(request, 'home/index.html')


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.username.lower()
            new_user.save()
            auth.login(request, new_user)
            messages.success(request, 'Account Created Successfully!')
            return redirect('home')
    context = {'form':form}
    return render(request, 'home/register.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You haven already loged-in!")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username = username, password = password)
        if auth_user is not None:
            auth.login(request, auth_user)
            messages.success(request, "Successfully Loged-In")
            return redirect('home')
        else:
            messages.error(request, "User doesn't Exists!")
            return redirect('login')
    return render(request, 'home/login.html')


def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, "You haven't Loged-In!")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "Successfilly Loged-Out!")
    return redirect('home')